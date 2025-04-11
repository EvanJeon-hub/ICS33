# Set 1 Problem 4
# Evan-Soobin Jeon
# 3537131
# ejeon2@uci.edu


class CustomTypeError(Exception):
    pass


class ExampleContextManager(Exception):
    def __init__(self, expected_exception):
        self.expected_exception = expected_exception

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is issubclass(exc_type, self.expected_exception):
            return True
        raise CustomTypeError(f"{self.expected_exception} is not raised"
                              f"but raised {exc_type if exc_type else 'no exception'}")


def should_raise(sample_exception):
    return ExampleContextManager(sample_exception)