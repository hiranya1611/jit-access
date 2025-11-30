import subprocess
import os
import logging

logging.basicConfig(filename="../logs/access.log",
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def grant_sudo_group(username):
    logging.info(f"Granting sudo access to {username}")
    subprocess.run(["sudo", "usermod", "-aG", "sudo", username], check=True)

def revoke_sudo_group(username):
    logging.info(f"Removing sudo access from {username}")
    subprocess.run(["sudo", "gpasswd", "-d", username, "sudo"], check=True)

def add_ssh_key(username, pubkey):
    logging.info(f"Adding SSH key for {username}")
    home = f"/home/{username}/.ssh"
    os.makedirs(home, exist_ok=True)
    auth = os.path.join(home, "authorized_keys")
    with open(auth, "a") as f:
        f.write(pubkey + "\n")
    os.chmod(auth, 0o600)

def remove_ssh_key(username, pubkey):
    logging.info(f"Removing SSH key for {username}")
    auth = f"/home/{username}/.ssh/authorized_keys"
    if not os.path.exists(auth):
        return
    with open(auth, "r") as f:
        lines = f.readlines()
    with open(auth, "w") as f:
        for l in lines:
            if pubkey.strip() != l.strip():
                f.write(l)
