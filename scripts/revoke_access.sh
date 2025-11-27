#!/bin/bash
USERNAME=$1

if [ -f /etc/sudoers.d/$USERNAME ]; then
    sudo rm /etc/sudoers.d/$USERNAME
    echo "[+] Access revoked for $USERNAME"
else
    echo "No sudo access found."
fi
