import json
from redis_connection import r
import redis

# Check Redis connection
if not r:
    print("Redis connection is unavailable.")
    exit()

def safe_redis_get(key, label):
    try:
        value = r.get(key)
        if value:
            print(f"\n{label}:")
            print(json.loads(value))
        else:
            print(f"{label} not found.")
    except redis.exceptions.RedisError as e:
        print(f"Redis error while retrieving {label}: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON for key '{key}'.")

# 1. Retrieve Computer Science department
safe_redis_get("departments:CompSci", "Computer Science Department")

# 2. Retrieve student Peter Lynch
safe_redis_get("students:Peter Lynch", "Student - Peter Lynch")

# 3. Retrieve course Data Engineering
safe_redis_get("courses:Data Engineering", "Course - Data Engineering")
