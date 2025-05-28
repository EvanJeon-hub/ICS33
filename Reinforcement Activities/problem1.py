# Evan-Soobin Jeon
# ejeon2@uci.edu
def partially_call(func, *p_args, **p_kwargs):
    def wrapper(*args, **kwargs):
        all_args = p_args + args
        all_kwargs = {**p_kwargs, **kwargs}
        return func(*all_args, **all_kwargs)
    return wrapper