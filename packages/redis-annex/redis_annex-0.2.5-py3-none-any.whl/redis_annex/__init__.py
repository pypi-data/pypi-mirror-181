from redis_annex.__about__ import __version__
from redis import Redis
from redis.asyncio.client import Pipeline
from typing import cast

def uadd(r: Redis, key, val) -> tuple[int | None, bool | None]:
    """add a value to a sorted set (key) that maintains insertion order via score (can be zero)"""
    idx: int | None = None
    new_val: bool | None = None

    def _uadd(pipe: Pipeline):
        nonlocal idx
        nonlocal new_val
        rank = cast(int, pipe.zrank(key, val))
        if rank is not None:
            new_val = False
        else:
            new_val = True
            rank = cast(int, pipe.zcard(key))
            pipe.multi()
            pipe.zadd(key, {val: rank})
        idx = rank

    r.transaction(_uadd, key)
    return idx, new_val


def add(r: Redis, key, val) -> int:
    """add a value to a list (key) and return its index"""
    return r.rpush(key, val) - 1
