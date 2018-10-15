from typing import Union

from lark.lexer import Token

from constructs import Constant, Namespace
from symboltable import IntType, Variable


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
    def __init__(self, target: Variable, source: Union[Variable, Constant]):
        self.target: Variable = target
        self.source: Union[Variable, Constant] = source

    def to_string(self) -> str:
        if isinstance(self.source, Variable):
            return f"scoreboard players operation {self.target.get_identifier()} = {self.source.get_identifier()}"
        else:
            if self.source.type == IntType():
                return f"scoreboard players set {self.target.get_identifier()} {self.source.value}"
            else:
                return f"scoreboard players set {self.target.get_identifier()} {bool_to_int(self.source.value)}"


class RunInstruction(Instruction):
    def __init__(self, command: str):
        self.command: str = command

    def to_string(self) -> str:
        return self.command


class EqualityInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"execute store success score {self.target.get_identifier()} if score {self.target.get_identifier()} = {self.source.get_identifier()}"


class UnequalityInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"execute store success score {self.target.get_identifier()} unless score {self.target.get_identifier()} = {self.source.get_identifier()}"


class LessThenInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"execute store success score {self.target.get_identifier()} if score {self.target.get_identifier()} < {self.source.get_identifier()}"


class LessThenEqualsInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"execute store success score {self.target.get_identifier()} if score {self.target.get_identifier()} <= {self.source.get_identifier()}"


class GreaterThenInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"execute store success score {self.target.get_identifier()} if score {self.target.get_identifier()} > {self.source.get_identifier()}"


class GreaterThenEqualsInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"execute store success score {self.target.get_identifier()} if score {self.target.get_identifier()} >= {self.source.get_identifier()}"


class AdditionInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"scoreboard players operation {self.target.get_identifier()} += {self.source.get_identifier()}"


class SubtractionInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"scoreboard players operation {self.target.get_identifier()} -= {self.source.get_identifier()}"


class MultiplicationInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"scoreboard players operation {self.target.get_identifier()} *= {self.source.get_identifier()}"


class DivisionInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"scoreboard players operation {self.target.get_identifier()} /= {self.source.get_identifier()}"


class ModuloInstruction(Instruction):
    def __init__(self, target: Variable, source: Variable):
        self.target: Variable = target
        self.source: Variable = source

    def to_string(self) -> str:
        return f"scoreboard players operation {self.target.get_identifier()} %= {self.source.get_identifier()}"


class Negateinstruction(Instruction):
    def __init__(self, variable: Variable):
        self.variable = variable

    def to_string(self):
        return f"scoreboard players operation {self.target.get_identifier()} /= {self.source.get_identifier()}"


class InvertInstruction(Instruction):
    def __init__(self, variable: Variable):
        self.variable = variable

    def to_string(self):
        return f"execute store success score {self.variable.get_identifier()} if score {self.variable.get_identifier()} 0"


class CallIfZeroInstruction(Instruction):
    def __init__(self, condition: Variable, namespace: Namespace, function_name: str):
        self.condition: Variable = condition
        self.namespace: Namespace = namespace
        self.function_name: str = function_name

    def to_string(self) -> str:
        return f"execute if score {self.condition.get_identifier()} matches 0 run function {self.namespace.name}:{self.function_name}"


class CallIfNotZeroInstruction(Instruction):
    def __init__(self, condition: Variable, namespace: Namespace, function_name: str):
        self.condition: Variable = condition
        self.namespace: Namespace = namespace
        self.function_name: str = function_name

    def to_string(self) -> str:
        return f"execute unless score {self.condition.get_identifier()} matches 0 run function {self.namespace.name}:{self.function_name}"


class CallInstruction(Instruction):
    def __init__(self, namespace: Namespace, function_name: str):
        self.namespace: Namespace = namespace
        self.function_name: str = function_name

    def to_string(self) -> str:
        return f"function {self.namespace.name}:{self.function_name}"
