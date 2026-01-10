#!/bin/bash
# Execute in cloud shell
ACCESS_TOKEN=$(gcloud auth print-access-token)
GOOGLE_CLOUD_PROJECT='pokeapi-215911'
CREATE_SLO_POST_BODY=$(cat <<EOF
{
  "displayName": "99% - Total/Bad Ratio - Rolling 30 days",
  "goal": 0.99,
  "rollingPeriod": "86400s",
  "serviceLevelIndicator": {
    "requestBased": {
      "goodTotalRatio": {
        "totalServiceFilter": "metric.type=\"logging.googleapis.com/user/function-executions\" resource.type=\"cloud_function\"",
        "badServiceFilter": "metric.type=\"logging.googleapis.com/user/function-crash\" resource.type=\"cloud_function\""
      }
    }
  }
}
EOF
)

curl  --http1.1 --header "Authorization: Bearer $ACCESS_TOKEN" --header "Content-Type: application/json" -X POST -d "$CREATE_SLO_POST_BODY" "https://monitoring.googleapis.com/v3/projects/$GOOGLE_CLOUD_PROJECT/services/_1QdRovaRBGqDhnMI8i2Yw/serviceLevelObjectives"