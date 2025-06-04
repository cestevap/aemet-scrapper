#!/bin/bash

WORKFLOW_NAME="Fetch AEMET Data Every 6 Hours"
MAX_RUNS=50  # You can increase this to get more runs
ARTIFACTS_DIR="artifacts"

mkdir -p "$ARTIFACTS_DIR"

echo "Fetching up to $MAX_RUNS runs for workflow: $WORKFLOW_NAME"

run_ids=$(gh run list --workflow="$WORKFLOW_NAME" --limit "$MAX_RUNS" --json databaseId -q '.[].databaseId')
echo "$runs_ids"

for run_id in $run_ids; do
    target_dir="$ARTIFACTS_DIR/$run_id"
    echo "Downloading artifacts for run $run_id into $target_dir"
    mkdir -p "$target_dir"
    gh run download "$run_id" --dir "$target_dir"
done

echo "✅ Download complete. Artifacts saved in ./$ARTIFACTS_DIR/"

