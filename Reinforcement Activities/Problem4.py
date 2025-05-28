# Evan-Soobin Jeon
# ejeon2@uci.edu
def make_repeater(func, count):
    def repeater(value):
        result = value
        for i in range(count):
            result = func(result)
        return result
    return repeater

def square(x):
    return x * x

single = make_repeater(square, 1)
print(single(3))