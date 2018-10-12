from __future__ import annotations

from typing import Dict, TYPE_CHECKING, List

from exception import UndeclaredVariableException, UndeclaredFunctionException, UndeclaredTypeException
from helper import singleton

if TYPE_CHECKING:
    from constructs import Namespace, VariableReference, TypeReference, FunctionReference


class Scope:
    def __init__(self):
        self.variables: Dict[str, Scope.Variable] = {}
        self.functions: Dict[str, Scope.Function] = {}
        self.types: Dict[str, Scope.Type] = {}

    def declare_variable(self, name: str, type: Scope.Type):
        raise NotImplementedError

    def declare_function(self, name: str):
        raise NotImplementedError

    def declare_class(self, name: str):
        raise NotImplementedError

    def has_variable(self, name: str) -> bool:
        return name in self.variables

    def has_function(self, name: str) -> bool:
        return name in self.functions

    def has_type(self, name: str) -> bool:
        return name in self.types

    def get_variable(self, name: str) -> Scope.Variable:
        return self.variables[name]

    def get_function(self, name: str) -> Scope.Function:
        return self.functions[name]

    def get_type(self, name: str) -> Scope.Type:
        return self.types[name]

    class Variable:
        def __init__(self, namespace: Namespace, name: str, type_: Scope.Type):
            self.namespace: Namespace = namespace
            self.name: str = name
            self.type: Scope.Type = type_

        def get_identifier(self) -> str:
            raise NotImplementedError

        def get_type(self) -> Scope.Type:
            return self.type

    class Function:
        def __init__(self, namespace: Namespace, name: str):
            self.namespace: Namespace = namespace
            self.name: str = name

        def get_identifier(self) -> str:
            raise NotImplementedError

    class Type:
        def __init__(self, namespace: Namespace, name: str):
            self.namespace: Namespace = namespace
            self.name: str = name


class GlobalScope(Scope):
    def __init__(self, namespace: Namespace):
        super().__init__()
        self.namespace: Namespace = namespace
        self.types["int"] = IntType.get_instance()
        self.types["boolean"] = BooleanType.get_instance()

    def declare_variable(self, name: str, type_: Scope.Type):
        self.variables[name] = self.GlobalVariable(self.namespace, name, type_)

    def declare_function(self, name: str):
        self.functions[name] = self.GlobalFunction(self.namespace, name)

    def declare_class(self, name: str):
        raise NotImplementedError

    class GlobalVariable(Scope.Variable):
        def get_identifier(self) -> str:
            return f"global {self.namespace.reference.name}.{self.name}"

    class GlobalFunction(Scope.Function):
        def get_identifier(self) -> str:
            return f"{self.namespace.reference.name}:{self.name}"

    class GlobalType(Scope.Type):
        pass


class BlockScope(Scope):
    def __init__(self, namespace: Namespace):
        super().__init__()
        self.namespace: Namespace = namespace

    def declare_variable(self, name: str, type_: Scope.Type):
        self.variables[name] = self.LocalVariable(self.namespace, name, type_)

    def declare_function(self, name: str):
        raise NotImplementedError

    def declare_class(self, name: str):
        raise NotImplementedError

    class LocalVariable(Scope.Variable):
        def get_identifier(self) -> str:
            return f"@e[type=armor_stand,tag=stack_frame,scores={{mfc.stack_depth=1}},limit=1] {self.namespace.reference.name}.{self.name}"


class ClassScope(Scope):
    def __init__(self):
        raise NotImplementedError


class BuiltinType(Scope.Type):
    def __init__(self, name: str):
        super().__init__(None, name)


@singleton
class IntType(BuiltinType):
    def __init__(self):
        super().__init__("int")


@singleton
class BooleanType(BuiltinType):
    def __init__(self):
        super().__init__("boolean")


class SymbolTable:
    def __init__(self):
        self.stack: List[Scope] = []

    def push(self, scope: Scope):
        self.stack.append(scope)

    def pop(self):
        self.stack.pop()

    def declare_variable(self, reference: VariableReference, type: Scope.Type):
        self.stack[-1].declare_variable(reference.name, type)

    def declare_function(self, reference: FunctionReference):
        self.stack[-1].declare_function(reference.name)

    def declare_class(self, reference: TypeReference):
        self.stack[-1].declare_class(reference.name)

    def search_variable(self, name: str) -> Scope.Variable:
        for env in reversed(self.stack):
            if env.has_variable(name):
                return env.get_variable(name)
        raise UndeclaredVariableException(name)

    def search_function(self, name: str) -> Scope.Function:
        for env in reversed(self.stack):
            if env.has_function(name):
                return env.get_function(name)
        raise UndeclaredFunctionException

    def search_type(self, name: str) -> Scope.Type:
        for env in reversed(self.stack):
            if env.has_type(name):
                return env.get_type(name)
        raise UndeclaredTypeException
