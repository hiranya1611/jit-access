from backend.database import get_db

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
