import json
import os
import redis

endpoint = 'redis://:p48c33a294b3863689cc537475c27ec398a544c022216bb4122b3c6dd8c6ecc29@ec2-52-54-111-142.compute-1.amazonaws.com:7090'

def get_redis_client():
    redis_client = redis.Redis.from_url(endpoint, decode_components=True)
    return redis_client

def get_data():
    filepath = os.path.join(os.path.abspath("merchants"), "data.json")

    with open(filepath, "r") as f:
        data = json.load(f)
    
    return data