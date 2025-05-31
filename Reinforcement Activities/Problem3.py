# Evan-Soobin Jeon
# ejeon2@uci.edu
import random

def cached(size):
    def decorator(func):
        cache = {}

        def helper(*args, **kwargs):
            try:
                key = (args, frozenset(kwargs.items()))
            except TypeError:
                return func(*args, **kwargs)

            if key in cache:
                return cache[key]

            result = func(*args, **kwargs)

            if len(cache) >= size:
                random_key = random.choice(list(cache.keys()))
                del cache[random_key]

            cache[key] = result
            return result
        return helper
    return decorator
