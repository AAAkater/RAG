from redis import StrictRedis

redis_client = StrictRedis(host="localhost", port="6379", db=0, decode_responses=True)


if __name__ == "__main__":
    redis_client.set("k1", "v1")

    v = redis_client.get("k1")

    print(v)
