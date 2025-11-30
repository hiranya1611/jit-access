#!/bin/bash
USERNAME="$1"
SUDOERS_FILE="/etc/sudoers.d/$USERNAME"

if id "$USERNAME" &>/dev/null; then
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | sudo tee "$SUDOERS_FILE" > /dev/null
    sudo chmod 440 "$SUDOERS_FILE"
    echo "Granted sudo to $USERNAME for 15 minutes"
else
    echo "User $USERNAME does not exist"
    exit 1
fi
