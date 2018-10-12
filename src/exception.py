from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from symboltable import Scope


class CompilerException(Exception):
    pass


class DuplicateClassException(CompilerException):
    pass


class DuplicateFunctionException(CompilerException):
    pass


class DuplicateVariableException(CompilerException):
    pass


class UndeclaredVariableException(CompilerException):
    def __init__(self, name):
        self.name = name


class UndeclaredFunctionException(CompilerException):
    pass


class UndeclaredTypeException(CompilerException):
    pass


class TypeMissmatchException(CompilerException):
    pass


class BadOperandException(CompilerException):
    def __init__(self, operand: str, *types: "Scope.Type"):
        if len(types) > 1:
            types_string = ", ".join([f"'{type.name}'" for type in types])
            super().__init__(f"Operand '{operand}' cannot be applied to types {types_string}")
        else:
            super().__init__(f"Operand '{operand}' cannot be applied to type '{types[0].name}'")
