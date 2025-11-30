#!/bin/bash
DB="../database/jit_access.db"

sqlite3 "$DB" "
SELECT u.username FROM access_requests ar
JOIN users u ON ar.user_id = u.id
WHERE ar.status = 'approved' 
  AND ar.approved_until < datetime('now')
" | while read user; do
    [ -n "$user" ] && bash scripts/revoke_access.sh "$user"
    sqlite3 "$DB" "UPDATE access_requests SET status='expired' WHERE user_id=(SELECT id FROM users WHERE username='$user') AND status='approved';"
done
