#!/bin/bash
USERNAME="$1"
SUDOERS_FILE="/etc/sudoers.d/$USERNAME"

if [ -f "$SUDOERS_FILE" ]; then
    sudo rm -f "$SUDOERS_FILE"
    echo "Revoked sudo from $USERNAME"
else
    echo "No active sudo rule for $USERNAME"
fi
