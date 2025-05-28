# Evan-Soobin Jeon
# ejeon2@uci.edu
def generate_range(start, end = None, step = 1):
    if end is None:
        end = start
        start = 0

    if step == 0:
        raise ValueError("Step cannot be zero.")

    if step > 0:
        while start < end:
            yield start
            start += step
    else:
        while start > end:
            yield start
            start += step

def no_fizz_without_buzz(start):
    i = start
    while True:
        if (i % 3 == 0 and i % 5 == 0) or (i % 3 != 0 and i % 5 != 0):
            yield i
        i += 1

def cartesian_product(*args):
    if not args:
        yield

    def product_helper(index, current):
        if index == len(args):
            yield current
            return

        for element in args[index]:
            yield from product_helper(index + 1, current + (element,))

    yield from product_helper(0, ())
