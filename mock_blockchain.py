import json
from datetime import datetime
import os

FILE = "mock_blockchain.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE,"r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)

def record_blockchain_event(action,file_id,user_id,file_hash):
    data = load_data()

    event = {
        "action": action,
        "file_id": file_id,
        "user_id": user_id,
        "file_hash": file_hash,
        "timestamp": str(datetime.utcnow())
    }

    data.append(event)
    save_data(data)

    print("[MOCK BLOCKCHAIN] Event recorded:",action)


def verify_file_integrity(file_id,file_hash):
    data = load_data()

    for e in data:
        if e["file_id"]==file_id and e["file_hash"]==file_hash:
            return {"verified":True}

    return {"verified":False}


def get_file_blockchain_history(file_id):
    data = load_data()
    return [e for e in data if e["file_id"]==file_id]


def get_user_blockchain_activity(user_id,limit=100):
    data = load_data()
    user_events=[e for e in data if e["user_id"]==user_id]
    return user_events[-limit:]


def is_blockchain_configured():
    return True