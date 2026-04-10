import redis

try:
    r = redis.Redis(host='localhost', port=6379)
    r.set("test", "hello") 
    print(r.get("test"))
except Exception as e:
    print(f"Error: {e}")