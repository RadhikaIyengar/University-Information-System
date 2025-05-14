import redis

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()  # test connection
except redis.exceptions.ConnectionError as e:
    print(f"Redis connection failed: {e}")
    r = None  # fallback
