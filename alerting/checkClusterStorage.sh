#!/bin/bash

# ===== CONFIG =====
OPENSEARCH_URL="https://localhost:9200"
AUTH="admin:Opensearch123!"
# LOG_FILE="/var/log/opensearch_disk_monitor.log"
LOG_FILE="/home/bikeride/opensearch/opensearch_disk_monitor.log"

# Thresholds
CRITICAL_THRESHOLD=90
WARN_THRESHOLD=75
FLOOD_STAGE_THRESHOLD=95
MIN_FREE_GB=10

# Get node stats
response=$(curl -s -k -u "$AUTH" "$OPENSEARCH_URL/_nodes/stats/fs")

# Current UTC timestamp
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Use jq to parse each node
echo "$response" | jq -r --arg timestamp "$timestamp" --argjson crit "$CRITICAL_THRESHOLD" \
  --argjson warn "$WARN_THRESHOLD" --argjson flood "$FLOOD_STAGE_THRESHOLD" \
  --argjson minfree "$MIN_FREE_GB" '
  .nodes | to_entries[] | 
  .value as $node | 
  {
    node: $node.name,
    disk_total_gb: ($node.fs.total.total_in_bytes / (1024*1024*1024)) | floor,
    disk_free_gb: ($node.fs.total.available_in_bytes / (1024*1024*1024)) | floor,
    disk_used_percent: (
      (1 - ($node.fs.total.available_in_bytes / $node.fs.total.total_in_bytes)) * 100
    ) | floor
  } | 
  .log_level = (
    if .disk_used_percent >= $flood or .disk_free_gb < $minfree then "critical"
    elif .disk_used_percent >= $crit then "critical"
    elif .disk_used_percent >= $warn then "warn"
    else "info"
    end
  ) | 
  .message = (
    "Disk usage is at \(.disk_used_percent)%"
    + (if .disk_used_percent >= $flood then " — approaching flood stage!" else "" end)
  ) | 
  .["@timestamp"] = $timestamp |
  @json
' >> "$LOG_FILE"
