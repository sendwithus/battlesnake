#!/bin/bash
# python lib/worker.py

PIDS=() # store forked pids here
NUM_PROCS=3  # Default to 3 procs

trap exiting SIGINT SIGTERM
function exiting() {
    # kill all pids
    for i in "${PIDS[@]}"; do
        kill -TERM $i;
        wait $i
    done
    exit 0
}

# fork $n procs
for i in $(seq 1 $NUM_PROCS); do
    echo "Starting worker #$i";
    python -u -m lib.worker &
    PIDS+=($!)
    sleep 0.1
done

# join all the processes
for i in "${PIDS[@]}"; do wait $i; done
