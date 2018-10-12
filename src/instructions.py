from typing import Union

from lark.lexer import Token

from constructs import Constant
from symboltable import Scope, IntType


def bool_to_int(boolean: Token) -> int:
    if boolean == "true":
        return 1
    elif boolean == "false":
        return 0
    else:
        assert False


class Instruction:
    def to_string(self) -> str:
        raise NotImplementedError


class StoreInstruction(Instruction):
    def __init__(self, target: Scope.Variable, source: Union[Scope.Variable, Constant]):
        self.target: Scope.Variable = target
        self.source: Union[Scope.Variable, Constant] = source

    def to_string(self) -> str:
        if isinstance(self.source, Scope.Variable):
            return f"scoreboard objectives operation {self.target.get_identifier()} = {self.source.get_identifier()}"
        else:
            if self.source.type == IntType.get_instance():
                return f"scoreboard objectives set {self.target.get_identifier()} {self.source.value}"
            else:
                return f"scoreboard objectives set {self.target.get_identifier()} {bool_to_int(self.source.value)}"


class RunInstruction(Instruction):
    def __init__(self, command: str):
        self.command: str = command

    def to_string(self) -> str:
        return self.command


class EqualityInstruction(Instruction):
    def __init__(self, target: Scope.Variable, source: Scope.Variable):
        self.target: Scope.Variable = target
        self.source: Scope.Variable = source

    def to_string(self) -> str:
        return f"execute store success score {self.target.get_identifier()} if score {self.target.get_identifier()} = {self.source.get_identifier()}"


class AdditionInstruction(Instruction):
    def __init__(self, target: Scope.Variable, source: Scope.Variable):
        self.target: Scope.Variable = target
        self.source: Scope.Variable = source

    def to_string(self) -> str:
        return f"scoreboard objectives operation {self.target.get_identifier()} += {self.source.get_identifier()}"


class IfInstruction(Instruction):
    def __init__(self, condition: Scope.Variable, target: Instruction):
        self.condition: Scope.Variable = condition
        self.target: Instruction = target

    def to_string(self) -> str:
        return f"execute if score {self.condition.get_identifier()} matches 1 run {self.target.to_string()}"


class IfNotInstruction(Instruction):
    def __init__(self, condition: Scope.Variable, target: Instruction):
        self.condition: Scope.Variable = condition
        self.target: Instruction = target

    def to_string(self) -> str:
        return f"execute if score {self.condition.get_identifier()} matches 0 run {self.target.to_string()}"


class CallInstruction(Instruction):
    def __init__(self, namespace: str, function_name: str):
        self.namespace: str = namespace
        self.function_name: str = function_name

    def to_string(self) -> str:
        return f"function {self.namespace}:{self.function_name}"
