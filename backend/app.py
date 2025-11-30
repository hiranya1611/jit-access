from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3, bcrypt

app = Flask(__name__,template_folder="../web/tempplates")
DB_PATH = "../database/jit_access.db"

def conn():
    return sqlite3.connect(DB_PATH)

@app.get("/")
def home():
    return "JIT Access Backend Running!"

@app.post("/register")
def register():
    data = request.json
    username, password = data["username"], data["password"]

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c = conn()
    cur = c.cursor()

    try:
        cur.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)",
                    (username, hashed, "USER"))
        c.commit()
        return jsonify({"success": True}), 201
    except:
        return jsonify({"error": "User already exists"}), 400
    finally:
        c.close()

@app.post("/request-access")
def request_access():
    data = request.json
    username, resource = data["username"], data["resource"]

    c = conn()
    cur = c.cursor()

    cur.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    now = datetime.now()
    expiry = now + timedelta(minutes=5)

    cur.execute("""INSERT INTO access_requests(user_id,resource,status,requested_at,expiry_time)
                   VALUES(?,?,?,?,?)""",
                (user[0], resource, "APPROVED", now, expiry))
    c.commit()
    c.close()

    return jsonify({"status": "approved", "valid_until": expiry}), 200

@app.get("/validate/<username>/<resource>")
def validate(username,resource):
    c = conn()
    cur = c.cursor()

    cur.execute("""
        SELECT expiry_time FROM access_requests ar
        JOIN users u ON ar.user_id = u.id
        WHERE u.username=? AND ar.resource=? AND status='APPROVED'
        ORDER BY id DESC LIMIT 1
    """,(username,resource))

    row = cur.fetchone()
    c.close()

    if not row:
        return jsonify({"access": False})

    if datetime.now() < datetime.fromisoformat(row[0]):
        return jsonify({"access": True})
    return jsonify({"access": False})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
