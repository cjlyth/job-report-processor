import json
import time

import numpy as np
import pandas as pd
import requests
import redis
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

client = redis.Redis(host="redis", port=6379, decode_responses=True)

URL = ("https://raw.githubusercontent.com/bsbodden/redis_vss_getting_started"
    "/main/data/bikes.json"
    )


def fetch_bikes():
    response = requests.get(URL, timeout=10)
    bikes = response.json()
    json.dumps(bikes[0], indent=2)
    
    pipeline = client.pipeline()
    for i, bike in enumerate(bikes, start=1):
        redis_key = f"bikes:{i:03}"
        pipeline.json().set(redis_key, "$", bike)
    res = pipeline.execute()

if __name__ == "__main__":
    fetch_bikes()