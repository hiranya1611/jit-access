#!/bin/bash

EXPIRED_USERS=$(sqlite3 database/jit_access.db "SELECT users.username FROM users JOIN access_requests ON users.id=access_requests.user_id WHERE access_requests.status='approved' AND approved_until < datetime('now');")

for user in $EXPIRED_USERS; do
    ./scripts/revoke_access.sh $user
    sqlite3 database/jit_access.db "UPDATE access_requests SET status='revoked' WHERE user_id=(SELECT id FROM users WHERE username='$user');"
    echo "[+] Auto revoked expired access for $user"
done
