# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import subprocess
from datetime import datetime
from backend.database import get_db, init_db
from backend.models import find_user, create_access_request, is_access_valid

app = Flask(__name__)
CORS(app)  # Allows your frontend to connect

SCRIPTS = {
    "grant": "../scripts/grant_access.sh",
    "revoke": "../scripts/revoke_access.sh"
}

def run_script(script_name, username):
    result = subprocess.run(["bash", SCRIPTS[script_name], username], capture_output=True, text=True)
    return result.returncode == 0

@app.get("/")
def home():
    return "JIT Access Management System – Backend Running!"

@app.post("/register")
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    db = get_db()
    try:
        db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   (username, hashed, "user"))
        db.commit()
        return jsonify({"success": True}), 201
    except:
        return jsonify({"error": "User already exists"}), 400
    finally:
        db.close()

@app.post("/login")
def login():
    data = request.json
    user = find_user(data.get("username"))
    if user and bcrypt.checkpw(data.get("password").encode(), user["password"].encode()):
        return jsonify({"login": True, "role": user["role"]})
    return jsonify({"login": False}), 401

@app.post("/request-access")
def request_access():
    data = request.json
    username = data.get("username")
    resource = data.get("resource", "sudo")

    user = find_user(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    create_access_request(user["id"], resource)

    # Auto-grant sudo for 15 minutes
    if run_script("grant", username):
        return jsonify({
            "status": "approved",
            "message": "Temporary sudo granted",
            "valid_until": (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        })
    return jsonify({"error": "Failed to grant access"}), 500

@app.get("/validate/<username>")
def validate(username):
    if is_access_valid(username):
        return jsonify({"access": True, "message": "Active"})
    run_script("revoke", username)  # Auto cleanup
    return jsonify({"access": False, "message": "Expired or revoked"})

if __name__ == "__main__":
	init_db()  #ensures tables exist
	app.run(host="0.0.0.0", port=5000, debug=False)
