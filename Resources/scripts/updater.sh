#!/bin/bash
# Executed when the master branch of PokeAPI/pokeapi gets updated
# Runs in CircleCI
# Generates new data using the latest changes of PokeAPI/pokeapi in order to open a Pull Request towards PokeAPI/api-data

set -o pipefail

org='PokeAPI'
data_repo='api-data'
engine_repo='pokeapi'
branch_name='staging'
username='pokeapi-machine-user'
email='pokeapi.co@gmail.com'
staging_environment_url='https://staging.pokeapi.co/api/v2/'
production_environment_url='https://pokeapi.co/api/v2/'
data_repo_url='https://github.com/PokeAPI/api-data'
engine_circleci_status_url='https://app.circleci.com/pipelines/github/PokeAPI/pokeapi'
deploy_circleci_status_url='https://app.circleci.com/pipelines/github/PokeAPI/deploy'

# Exit the script notifying the user about its success
cleanexit() {
	echo "Exiting"
	echo "$2"
  if [ "$1" -gt "0" ]; then
    notify_engine_pr "end_failed"
  else
    notify_engine_pr "end_success"
  fi
	exit $1
}

# Create and use a personal folder
prepare() {
  mkdir -p ./repositories
  cd repositories || cleanexit 1 "Failed to cd"
}

# GraphQL query to retrieve a PR's number based on a commit hash
pr_associated_with_sha_graphql_query_content() {
  cat <<EOF
query associatedPRs {
  repository(name: \"pokeapi\", owner: \"PokeAPI\") {
    commit: object(expression: \"$1\") {
      ... on Commit {
        associatedPullRequests(first: 1) {
          edges {
            node {
              number
            }
          }
        }
      }
    }
  }
}
EOF
}

# Get the PR's numer associated with the last commit
get_invokator_pr_number_from_graphql() {
  last_commit_sha="$(git rev-parse HEAD)"
  query="$(pr_associated_with_sha_graphql_query_content "$last_commit_sha")"
  query=$(echo $query) # echo strips all IFS characters (newline, space)
  pr_number=$(curl -s -H "Content-Type: application/json" -H "Authorization: token $MACHINE_USER_GITHUB_API_TOKEN" -X POST --data "{\"query\": \"$query\"}" "https://api.github.com/graphql" | jq ".data.repository.commit.associatedPullRequests.edges[0].node.number" )
  echo "$pr_number"
}

# Check and return the number of the Pull Request that started this job
get_invokator_pr_number() {
  commit_msg_regex="Merge pull request #([0-9]+) from PokeAPI/(.*)"
  last_commit_message=$(git log --oneline --format=%B -n 1 HEAD | head -n 1)
  invokator_pr_number_from_graphql="$(get_invokator_pr_number_from_graphql)"
  if ! [ -z "$CIRCLE_PULL_REQUEST" ]; then
    echo "${CIRCLE_PULL_REQUEST##*/}"
  elif [ "$invokator_pr_number_from_graphql" != 'null' ]; then
    echo "$invokator_pr_number_from_graphql"
  elif [[ $last_commit_message =~ $commit_msg_regex ]]; then
    echo "${BASH_REMATCH[1]}"
  else
    echo 'null'
  fi
}

# Clone the repository containing the static JSON files
clone() {
  git clone "https://github.com/${org}/${data_repo}.git" "$data_repo"
}

# Configure git to use the supplied user when committing
configure_git() {
  git config --global user.name "$username"
  git config --global user.email "$email"
}

pr_input_updater_start() {
  cat <<EOF
{
  "body": "A [PokeAPI/api-data](${data_repo_url}) refresh has started. In 45 minutes the staging branch of [PokeAPI/api-data](${data_repo_url}/tree/staging) will be pushed with the new generated data. <br><br> The staging branch will be deployed in our [staging environment]($staging_environment_url) and you will be able to review the entire API. <br><br> A Pull Request ([master](${data_repo_url}/tree/master)<-[staging](${data_repo_url}/tree/staging)) will be also created at [PokeAPI/api-data](${data_repo_url}/pulls) and assigned to the PokeAPI Core team to be reviewed. If approved and merged new data will soon be available worldwide at [pokeapi.co]($production_environment_url)"
}
EOF
}

pr_input_updater_end_success() {
  cat <<EOF
{
  "body": "The updater script has finished its job and has now opened a Pull Request towards [PokeAPI/api-data](${data_repo_url}/pulls) with the updated data. <br><br> You can see the Pull Request deployed at our [staging environment]($staging_environment_url) when [CircleCI deploy]($deploy_circleci_status_url) will be finished (_check the started time of the last build_)"
}
EOF
}

pr_input_updater_end_failed() {
  cat <<EOF
{
  "body": "The updater script couldn't finish its job. Please check [CircleCI's builds]($engine_circleci_status_url) and [logs](${CIRCLE_BUILD_URL})."
}
EOF
}

# If the job was started by a Pull Request, add a comment to notify the users
notify_engine_pr() {
  if [[ $1 == "start" || $1 == "end_failed" || $1 == "end_success" ]]; then
    engine_repo_pr_number=$(get_invokator_pr_number)
    if [ "$engine_repo_pr_number" != "null" ]; then
      curl -f -H "Authorization: token $MACHINE_USER_GITHUB_API_TOKEN" -X POST --data "$(pr_input_updater_$1)" "https://api.github.com/repos/$org/$engine_repo/issues/$engine_repo_pr_number/comments"
    fi
  fi
}

# Run the updater script (https://github.com/PokeAPI/api-data/blob/master/updater/cmd.bash) which will generate the new pokeapi data and push it to the api-data repository under a new branch
run_updater() {
  cd "$data_repo/updater" || cleanexit 1 "Failed to cd"
  # Wait to be sure PokeAPI/pokeapi's master branch has been updated on Github with the lastest merged PR content
  sleep 10

  # Build the updater image
  docker build -t pokeapi-updater .
  if [ $? -ne 0 ]; then
    cleanexit 1 "Failed to build the pokeapi-updater image"
  fi

  # Run the updater
  docker run --privileged -e COMMIT_EMAIL="$email" -e COMMIT_NAME="$username" -e BRANCH_NAME="$branch_name" -e REPO_POKEAPI="https://github.com/$org/$engine_repo.git" -e REPO_DATA="https://$MACHINE_USER_GITHUB_API_TOKEN@github.com/$org/$data_repo.git" pokeapi-updater
  if [ $? -ne 0 ]; then
    cleanexit 1 "Failed to run the pokeapi-updater container"
  fi

  cd .. || cleanexit 1 "Failed to cd"
}

# Check if the updater script has pushed the data to a new branch
check_remote_branch() {
  # Wait for Github to update origin/${branch_name}
  sleep 10

  curl -f -H "Authorization: token $MACHINE_USER_GITHUB_API_TOKEN" -X GET "https://api.github.com/repos/$org/$data_repo/branches/$1"
  if [ $? -ne 0 ]; then
    cleanexit 1 "The updater script failed to push the new data"
  fi
}

# Generate the input content that will be sent to Github's API to open a refresh-data PR towards PokeAPI/api-data
pr_input_content_with_pr_number() {
  cat <<EOF
{
  "title": "API data update from \`${org}/${engine_repo}#${1}\`",
  "body": "Incoming data generated by [${org}/${engine_repo}](https://github.com/${org}/${engine_repo})'s CircleCI worker since Pull Request [#${1}](https://github.com/${org}/${engine_repo}/pull/${1}) was merged into the \`master\` branch. <br><br> The new data was generated using a copy of [${org}/${engine_repo}](https://github.com/${org}/${engine_repo}/commits/master) repository when the \`HEAD\` was pointing to \`${CIRCLE_SHA1}\`. <br><br> This Pull Request should have been deployed in our [staging environment]($staging_environment_url), check [here]($deploy_circleci_status_url) for the lastest build timestamp and status code.",
  "head": "$branch_name",
  "base": "master",
  "assignees": [
    "Naramsim"
  ],
  "labels": [
    "api-data-update"
  ]
}
EOF
}

# Copy of pr_input_content_with_pr_number
# run when the script cannot detect the merged PR number that started the CircleCI job
pr_input_content_without_pr_number() {
  cat <<EOF
{
  "title": "API data update from \`${org}/${engine_repo}\`",
  "body": "Incoming data generated by [${org}/${engine_repo}](https://github.com/${org}/${engine_repo})'s CircleCI worker. <br><br> The new data was generated using a copy of [${org}/${engine_repo}](https://github.com/${org}/${engine_repo}/commits/master) repository when the \`HEAD\` was pointing to \`${CIRCLE_SHA1}\`. <br><br> This Pull Request should have been deployed in our [staging environment]($staging_environment_url), check [here]($deploy_circleci_status_url) for the lastest build timestamp and status code.",
  "head": "$branch_name",
  "base": "master",
  "assignees": [
    "Naramsim"
  ],
  "labels": [
    "api-data-update"
  ]
}
EOF
}

# Create a Pull Request to merge the branch recently pushed by the updater with the master branch
create_pr() {
  engine_repo_pr_number=$(get_invokator_pr_number)
  if [ "$engine_repo_pr_number" != "null" ]; then
    data_repo_pr_number=$(curl -H "Authorization: token $MACHINE_USER_GITHUB_API_TOKEN" -X POST --data "$(pr_input_content_with_pr_number "$engine_repo_pr_number")" "https://api.github.com/repos/$org/$data_repo/pulls" | jq '.number')
  else
    data_repo_pr_number=$(curl -H "Authorization: token $MACHINE_USER_GITHUB_API_TOKEN" -X POST --data "$(pr_input_content_without_pr_number)" "https://api.github.com/repos/$org/$data_repo/pulls" | jq '.number')
  fi
  if [[ "$data_repo_pr_number" = "null" ]]; then
    cleanexit 1 "Couldn't create the Pull Request"
  fi
  echo "$data_repo_pr_number"
}

pr_input_assignees_and_labels() {
  cat <<EOF
{
  "assignees": [
    "Naramsim"
  ],
  "labels": [
    "api-data-update"
  ]
}
EOF
}

# Assign the PR to Naramsim and add a label
customize_pr() {
  # Wait for Github to open the PR
  sleep 10
  
  data_repo_pr_number=$1
  curl -H "Authorization: token $MACHINE_USER_GITHUB_API_TOKEN" -X PATCH --data "$(pr_input_assignees_and_labels)" "https://api.github.com/repos/$org/$data_repo/issues/$data_repo_pr_number"
  if [ $? -ne 0 ]; then
		echo "Couldn't add Assignees and Labes to the Pull Request"
	fi
}

pr_input_reviewers() {
  cat <<EOF
{
  "reviewers": [
    "Naramsim"
  ],
  "team_reviewers": [
    "core-team"
  ]
}
EOF
}

# Request the Core team to review the Pull Request
add_reviewers_to_pr() {
  data_repo_pr_number=$1
  curl -H "Authorization: token $MACHINE_USER_GITHUB_API_TOKEN" -X POST --data "$(pr_input_reviewers)" "https://api.github.com/repos/$org/$data_repo/pulls/$data_repo_pr_number/requested_reviewers"
  if [ $? -ne 0 ]; then
    echo "Couldn't add Reviewers to the Pull Request"
  fi
}

prepare
configure_git
clone
notify_engine_pr "start"
run_updater
check_remote_branch "$branch_name"
if [ "$CIRCLE_BRANCH" = 'master' ]; then
  sleep 300 # 5 minutes, the time it takes for CircleCI's api-data script to generate the data and for CircleCI's deploy script to deploy it to the staging environment
  check_remote_branch "$branch_name"
  data_repo_pr_number=$(create_pr)
  customize_pr "$data_repo_pr_number"
  add_reviewers_to_pr "$data_repo_pr_number"
fi
cleanexit 0 'Done'
