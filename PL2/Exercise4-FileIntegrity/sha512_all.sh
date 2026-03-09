#!/bin/bash
# PL2 Exercise 4: Generate SHA-512 of all files under a directory; time the run.
# Usage: ./sha512_all.sh [directory]
#        Default directory is current (.). Use time ./sha512_all.sh /path to measure.

DIR="${1:-.}"
if [ ! -d "$DIR" ]; then
  echo "Not a directory: $DIR"
  exit 1
fi

echo "Start: $(date -Iseconds)"
START=$(date +%s)

find "$DIR" -type f -print0 | while IFS= read -r -d '' f; do
  sha512sum "$f" 2>/dev/null || true
done

END=$(date +%s)
echo "End: $(date -Iseconds)"
echo "Elapsed: $((END - START)) seconds"
