# Set 1 Problem 4
# Evan-Soobin Jeon
# 3537131
# ejeon2@uci.edu
class CustomTypeError(Exception):
    pass

class ExampleContextManager(Exception):
    pass

def should_raise(sample_exception):
    return ExampleContextManager(sample_exception)