import requests
import time
from datetime import datetime

N8N_WEBHOOK = "http://localhost:5678/webhook/a5995e57-6bcc-41f1-b50b-61efc00abc7a"
AW_API = "http://localhost:5600/api/0"


def get_window_bucket():
    buckets = requests.get(f"{AW_API}/buckets").json()
    for bucket_id in buckets.keys():
        if "aw-watcher-window" in bucket_id:
            return bucket_id
    return None


def get_afk_bucket():
    buckets = requests.get(f"{AW_API}/buckets").json()
    for bucket_id in buckets.keys():
        if "aw-watcher-afk" in bucket_id:
            return bucket_id
    return None


WINDOW_BUCKET = get_window_bucket()
AFK_BUCKET = get_afk_bucket()
print("Using window bucket:", WINDOW_BUCKET)
print("Using AFK bucket:", AFK_BUCKET)


def is_afk():
    """Check if user is AFK in the last minute"""
    if not AFK_BUCKET:
        return False
    
    try:
        events = requests.get(
            f"{AW_API}/buckets/{AFK_BUCKET}/events?limit=1"
        ).json()
        
        if not events:
            return False
        
        # If status is "afk", user is away
        return events[0]["data"].get("status") == "afk"
    except:
        return False


def get_active_window():
    if not WINDOW_BUCKET:
        return None

    # Check if user is AFK first
    if is_afk():
        return {
            "app_name": "AFK",
            "window_title": "Away From Keyboard",
            "url": "Not captured",
            "duration_seconds": 60,
            "timestamp": datetime.now().isoformat()
        }

    try:
        events = requests.get(
            f"{AW_API}/buckets/{WINDOW_BUCKET}/events?limit=1"
        ).json()

        if not events:
            return None

        e = events[0]
        
        # Extract URL if available (Chrome/Firefox)
        url = e["data"].get("url", "Not captured")

        return {
            "app_name": e["data"].get("app", "Unknown"),
            "window_title": e["data"].get("title", "Unknown"),
            "url": url,
            "duration_seconds": 60,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as err:
        print(f"Error getting window: {err}")
        return None


print("Starting activity tracker...")
while True:
    try:
        data = get_active_window()
        if data:
            response = requests.post(N8N_WEBHOOK, json=data)
            print(f"Sent: {data['app_name']} - {data['window_title'][:50]}")
    except Exception as err:
        print("Error:", err)

    time.sleep(60)