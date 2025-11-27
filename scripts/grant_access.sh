#!/bin/bash

USERNAME=$1

if id "$USERNAME" &>/dev/null; then
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$USERNAME
    echo "[+] Granted temporary sudo access to $USERNAME"
else
    echo "User does not exist"
fi
