




def should_raise(expected_exc_type):
    return _ShouldRaiseContext(expected_exc_type)


class MissingExpectedError(Exception):
    pass


class _ShouldRaiseContext:
    def __init__(self, expected_exc_type):
        self._expected_exc_type = expected_exc_type


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is self._expected_exc_type:
            return True
        else:
            # Later this quarter, we'll learn how to outfit our exceptions
            # with custom error messages.
            raise MissingExpectedError






