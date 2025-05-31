# Evan-Soobin Jeon
# ejeon2@uci.edu
import random

def cached(size):
    def decorator(func):
        cache = {}
        def wrapper(*args, **kwargs):
            try:
                key = (args, frozenset(kwargs.items()))
            except TypeError:
                return func(*args, **kwargs)

            if key in cache:
                return cache[key]

            if len(cache) >= size:
                ramdom_k = random.choice(list(cache.keys()))
                del cache[ramdom_k]

            cache[key] = result
            return result

        return wrapper
    return decorator