import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_cached_text(trial_id: str) -> str | None:
    key = f"trial:{trial_id}"
    return r.get(key)

def cache_text(trial_id: str, text: str):
    key = f"trial:{trial_id}"
    r.set(key, text)