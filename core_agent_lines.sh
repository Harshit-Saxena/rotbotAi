#!/bin/bash
# Count core agent lines of code (excluding tests, templates, and markdown)
echo "rotbot core agent line count:"
echo "=============================="
find rotbot/ -name "*.py" -not -path "*/test*" | sort | while read f; do
    lines=$(wc -l < "$f")
    printf "  %-50s %5d\n" "$f" "$lines"
done
echo "------------------------------"
total=$(find rotbot/ -name "*.py" -not -path "*/test*" -exec cat {} + | wc -l)
echo "  TOTAL: $total lines"
