import threading
import time
import subprocess
import os
from datetime import datetime
import notifier
import queue_manager

# Map usernames to emails for notifications
USER_EMAILS = {
    "admin": "admin@example.com",
    # add your users here
}

WEBHOOK_URL = "https://example.com/webhook"  # Change this to your webhook URL or remove

def run_jobs_background(jobs, lock):
    while True:
        try:
            with lock:
                pending_jobs = [job for job in jobs if job.status == "pending"]
                if not pending_jobs:
                    job = None
                else:
                    job = pending_jobs[0]

            if job:
                print(f"[Runner] Starting job {job.id}")
                job.status = "running"
                job.started_at = datetime.now().isoformat()

                with lock:
                    queue_manager.save_queue(jobs)

                hash_file_path = os.path.join("uploads", job.hash_file)
                wordlist_path = os.path.join("wordlists", job.wordlist)
                rule_path = os.path.join("rules", job.rule) if job.rule else None

                cmd = [
                    "hashcat",
                    "-m", str(job.hash_type),
                    hash_file_path,
                    wordlist_path,
                ]

                if rule_path:
                    cmd.extend(["-r", rule_path])

                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    job.result = result.stdout.strip()
                    job.status = "finished"
                    print(f"[Runner] Job {job.id} finished.")
                except subprocess.CalledProcessError as e:
                    job.status = "failed"
                    job.result = e.stderr.strip()
                    print(f"[Runner] Job {job.id} failed: {job.result}")

                job.finished_at = datetime.now().isoformat()

                with lock:
                    queue_manager.save_queue(jobs)

                # Send notifications
                user_email = USER_EMAILS.get(job.username)
                if user_email:
                    subject = f"Hashcat Job {job.id} - {job.status.capitalize()}"
                    message = (
                        f"Job ID: {job.id}\n"
                        f"Status: {job.status}\n"
                        f"Result:\n{job.result}\n"
                        f"Started: {job.started_at}\n"
                        f"Finished: {job.finished_at}\n"
                    )
                    notifier.send_email(user_email, subject, message)

                if WEBHOOK_URL:
                    payload = {
                        "job_id": job.id,
                        "status": job.status,
                        "username": job.username,
                        "result": job.result,
                    }
                    notifier.send_webhook(WEBHOOK_URL, payload)

            else:
                time.sleep(3)
        except Exception as e:
            print(f"[Runner Exception]: {e}")
            time.sleep(5)


def start_runner(jobs, lock):
    thread = threading.Thread(target=run_jobs_background, args=(jobs, lock), daemon=True)
    thread.start()
    print("[Runner] Background thread started.")
