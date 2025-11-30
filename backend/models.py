# backend/models.py
from backend.database import get_db
from datetime import datetime

def find_user(username):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    db.close()
    return user

def create_access_request(user_id, resource="sudo"):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO access_requests (user_id, resource, status) VALUES (?, ?, 'approved')",
        (user_id, resource)
    )
    cur.execute("UPDATE access_requests SET approved_until = datetime('now', '+15 minutes') WHERE id = last_insert_rowid()")
    db.commit()
    db.close()

def get_latest_request(username, resource="sudo"):
    db = get_db()
    row = db.execute("""
        SELECT ar.* FROM access_requests ar
        JOIN users u ON ar.user_id = u.id
        WHERE u.username = ? AND ar.resource = ?
        ORDER BY ar.id DESC LIMIT 1
    """, (username, resource)).fetchone()
    db.close()
    return row

def is_access_valid(username, resource="sudo"):
    request = get_latest_request(username, resource)
    if not request or request['status'] != 'approved':
        return False
    expiry = request['approved_until']
    return datetime.fromisoformat(expiry) > datetime.now() if expiry else Falsefrom backend.database import get_db

def get_user(username):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def create_request(user_id):
    conn = get_db()
    conn.execute("INSERT INTO access_requests (user_id, status) VALUES (?, 'pending')", (user_id,))
    conn.commit()
    conn.close()

def approve_request(request_id, approved_until):
    conn = get_db()
    conn.execute("UPDATE access_requests SET status='approved', approved_until=? WHERE id=?", (approved_until, request_id))
    conn.commit()
    conn.close()

def revoke_request(request_id):
    conn = get_db()
    conn.execute("UPDATE access_requests SET status='revoked' WHERE id=?", (request_id,))
    conn.commit()
    conn.close()
