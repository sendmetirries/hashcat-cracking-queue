import pickle
import os
from job_model import Job

QUEUE_FILE = "queue.pkl"

def save_queue(jobs):
    # Serialize list of Job objects by saving their dicts
    with open(QUEUE_FILE, "wb") as f:
        # Save list of dicts
        pickle.dump([job.to_dict() for job in jobs], f)

def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "rb") as f:
        jobs_data = pickle.load(f)
        # Convert dicts back to Job objects
        return [Job.from_dict(data) for data in jobs_data]
