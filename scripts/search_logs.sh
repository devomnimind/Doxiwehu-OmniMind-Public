#!/bin/bash
# Search for OmniMind-related keywords in /var/log/syslog and /var/log/kern.log
# excluding potential noise

grep -iE "omnimind|phi|s3!|sovereign" /var/log/syslog | tail -n 50
echo "--- KERN LOG ---"
grep -iE "omnimind|phi|s3!|sovereign" /var/log/kern.log | tail -n 50
