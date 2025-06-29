import uuid
from datetime import datetime

class Job:
    def __init__(self, username, hash_file, hash_type, wordlist, rule=None):
        self.id = str(uuid.uuid4())
        self.username = username
        self.hash_file = hash_file
        self.hash_type = hash_type
        self.wordlist = wordlist
        self.rule = rule

        self.status = "pending"  # pending, running, finished, failed
        self.result = None
        self.created_at = datetime.now().isoformat()
        self.started_at = None
        self.finished_at = None

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "hash_file": self.hash_file,
            "hash_type": self.hash_type,
            "wordlist": self.wordlist,
            "rule": self.rule,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }

    @classmethod
    def from_dict(cls, data):
        job = cls(
            username=data["username"],
            hash_file=data["hash_file"],
            hash_type=data["hash_type"],
            wordlist=data["wordlist"],
            rule=data.get("rule")
        )
        job.id = data["id"]
        job.status = data.get("status", "pending")
        job.result = data.get("result")
        job.created_at = data.get("created_at")
        job.started_at = data.get("started_at")
        job.finished_at = data.get("finished_at")
        return job
