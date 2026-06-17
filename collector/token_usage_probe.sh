#!/usr/bin/env bash
# Run this ON YOUR MAC (Terminal) and paste me the output.
# It tells us whether Cowork stores per-turn token usage on disk (the only way to get real cost numbers).
DIR="$HOME/Library/Application Support/Claude"
echo "== searching for session files under: $DIR =="
FILES=$(find "$DIR" -type f \( -name "*.jsonl" -o -name "*.json" \) 2>/dev/null | grep -i -E "session|transcript|message|conversation" | head -5)
echo "$FILES"
echo
echo "== sample keys / token fields in the first file =="
F=$(echo "$FILES" | head -1)
if [ -n "$F" ]; then
  echo "file: $F"
  head -c 4000 "$F" 2>/dev/null | grep -o -i -E '"(usage|input_tokens|output_tokens|model|total_tokens|cache_[a-z_]*tokens)"' | sort | uniq -c
else
  echo "No session files found at that path — tell me and I'll widen the search."
fi
