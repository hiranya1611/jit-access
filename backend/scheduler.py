from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from backend.database import get_db
from backend.access_manager import remove_ssh_key, revoke_sudo_group
import logging

logging.basicConfig(filename="../logs/access.log", 
                    level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

scheduler = BackgroundScheduler()
scheduler.start()

def revoke_job(request_id, username, pubkey):
    logging.info(f"Revoking access for {username} (request {request_id})")

    if pubkey:
        remove_ssh_key(username, pubkey)
    else:
        revoke_sudo_group(username)

    db = get_db()
    db.execute("UPDATE access_requests SET status='REVOKED' WHERE id=?", (request_id,))
    db.commit()
    db.close()

def schedule_revocation(request_id, username, end_time, pubkey):
    run_dt = datetime.fromisoformat(end_time)
    scheduler.add_job(revoke_job, 'date', run_date=run_dt,
                      args=[request_id, username, pubkey])
    logging.info(f"Scheduled revoke for {username} at {run_dt}")

def load_existing_jobs():
    db = get_db()
    rows = db.execute(
        "SELECT id, username, end_time, pubkey FROM access_requests WHERE status='APPROVED'"
    ).fetchall()
    db.close()

    for r in rows:
        schedule_revocation(r["id"], r["username"], r["end_time"], r["pubkey"])

load_existing_jobs()
