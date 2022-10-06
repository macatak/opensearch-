#!/bin/bash

# TODO
# accept commandline args
# ??? do we want to set an ID??? pros/cons

# monitor name
MONITOR_NAME="spam_eggs1"

# the target index
TARGET_INDEX="test_index_ingest"
# the field to run the query against
FIELD_NAME="log_level"
# the search term for the field
SEARCH_TERM="fatal"
# the time range to go back and search
# minutes=m, hours=h
# number is value
# this searches over the last hour
TIME_RANGE="-1h" 
# threshold for the number of hits
# anything greater than 5 will trigger
LIMIT_VALUE=5
# how often the monitor will run
RUN_INTERVAL_VALUE="10"
# MINUTES, HOURS, etc.
RUN_INTERVAL_UNIT="MINUTES"

curl -XPOST -u admin:admin --insecure  "https://localhost:9200/_plugins/_alerting/monitors?pretty" -H "Content-Type:application/json" -d"{
  \"name\": \"$MONITOR_NAME\",
  \"enabled\": true,
  \"inputs\": [
    {
      \"search\": {
        \"indices\": [
          \"$TARGET_INDEX\"
        ],
        \"query\": {
          \"size\": 0,
          \"aggregations\": {},
          \"query\": {
            \"bool\": {
              \"filter\": {
                \"range\": {
                  \"@timestamp\": {
                    \"from\": \"||-$TIME_RANGE\",
                    \"to\": \"\"
                  }
                }
              },
              \"must\": {
                \"term\": {
                  \"$FIELD_NAME\": \"$SEARCH_TERM\"
                }
              }
            }
          }
        }
      }
    }
  ],
  \"schedule\": {
    \"period\": {
      \"interval\": $RUN_INTERVAL_VALUE,
      \"unit\": \"$RUN_INTERVAL_UNIT\"
    }
  },
  \"triggers\": [
    {
      \"name\": \"curl_count-trigger\",
      \"severity\": \"1\",
      \"condition\": {
        \"script\": {
          \"source\": \"ctx.results[0].hits.total.value > $LIMIT_VALUE\",
          \"lang\": \"painless\"
        }
      },
      \"actions\": [{
        \"name\": \"notification_api_1\",
        \"destination_id\": \"notification_api_1\",
        \"message_template\": {
        \"source\": \"Monitor {{ctx.monitor.name}} just entered alert status\"
        }
      }]
    }
  ]
}"
