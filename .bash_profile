
parse_git_branch() {

	git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

export PS1="[\W]\[\033[32m\]\$(parse_git_branch)\[\033[00m\] $ "