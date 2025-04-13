def only_truthy(**kwargs):
    result = {}

    for name, value in kwargs.items():
        if value:
            result[f'_{name}'] = value

    return result