_TRUE_VALUES = ["1", "true", "yes"]
_FALSE_VALUES = ["0", "false", "no"]


class Bool:
    def __new__(cls, *args, **kwargs):
        if isinstance(args[0], bool):
            return args[0]

        value: str = args[0].lower()
        if value in _TRUE_VALUES:
            return True
        elif value in _FALSE_VALUES:
            return False

        raise ValueError
