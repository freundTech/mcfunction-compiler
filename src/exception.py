class DuplicateClassException(Exception):
    pass


class DuplicateFunctionException(Exception):
    pass


class DuplicateVariableException(Exception):
    pass


class UndeclaredVariableException(Exception):
    def __init__(self, name):
        self.name = name

class UndeclaredFunctionException(Exception):
    pass


class UndeclaredTypeException(Exception):
    pass
