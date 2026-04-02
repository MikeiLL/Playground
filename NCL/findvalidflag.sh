#!/bin/bash
for f in flag_*.exe; do
    if osslsigncode verify -in "$f" -CAfile ca.crt | grep -q "Signature verification: ok"; then
        echo "Valid flag found in $f"
        break
    fi
done