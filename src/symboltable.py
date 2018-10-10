from exception import UndeclaredVariableException, UndeclaredFunctionException, UndeclaredTypeException


class Scope:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.types = {}

    def declare_variable(self, name, type):
        raise NotImplementedError

    def declare_function(self, name):
        raise NotImplementedError

    def declare_class(self, name):
        raise NotImplementedError

    def has_variable(self, name):
        return name in self.variables

    def has_function(self, name):
        return name in self.functions

    def has_type(self, name):
        return name in self.types

    def get_variable(self, name):
        return self.variables[name]

    def get_function(self, name):
        return self.functions[name]

    def get_type(self, name):
        return self.types[name]

    class Variable:
        def __init__(self, namespace, name, type_):
            self.namespace = namespace
            self.name = name
            self.type = type_

        def get_identifier(self):
            raise NotImplementedError

        def get_type(self):
            return self.type

    class Function:
        def __init__(self, namespace, name):
            self.namespace = namespace
            self.name = name

        def get_identifier(self):
            raise NotImplementedError

    class Type:
        def __init__(self, namespace, name):
            self.namespace = namespace
            self.name = name

        def __eq__(self, other):
            if self.__class__ != other.__class__:
                return False
            return self.name == other.name and self.namespace == other.namespace


class GlobalScope(Scope):
    def __init__(self, namespace):
        super().__init__()
        self.namespace = namespace
        self.types["int"] = self.intType
        self.types["boolean"] = self.booleanType

    def declare_variable(self, name, type_):
        self.variables[name] = self.GlobalVariable(self.namespace, name, type_)

    def declare_function(self, name):
        self.functions[name] = self.GlobalFunction(self.namespace, name)

    def declare_class(self, name):
        raise NotImplementedError

    class GlobalVariable(Scope.Variable):
        def get_identifier(self):
            return f"global {self.namespace.reference.name}.{self.name}"

    class GlobalFunction(Scope.Function):
        def get_identifier(self):
            return f"{self.namespace.reference.name}:{self.name}"

    class GlobalType(Scope.Type):
        pass

    intType = GlobalType(None, "int")
    booleanType = GlobalType(None, "boolean")


class BlockScope(Scope):
    def __init__(self, namespace):
        super().__init__()
        self.namespace = namespace

    def declare_variable(self, name, type_):
        self.variables[name] = self.LocalVariable(self.namespace, name, type_)

    def declare_function(self, name):
        raise NotImplementedError

    def declare_class(self, name):
        raise NotImplementedError

    class LocalVariable(Scope.Variable):
        def get_identifier(self):
            return f"@e[type=armor_stand,tag=stack_frame,scores={{mfc.stack_depth=1}},limit=1] {self.namespace.reference.name}.{self.name}"


class ClassScope(Scope):
    def __init__(self):
        raise NotImplementedError


class SymbolTable:
    def __init__(self):
        self.stack = []

    def push(self, scope):
        self.stack.append(scope)

    def pop(self):
        self.stack.pop()

    def declare_variable(self, reference, type):
        self.stack[-1].declare_variable(reference.name, type)

    def declare_function(self, reference):
        self.stack[-1].declare_function(reference.name)

    def declare_class(self, reference):
        self.stack[-1].declare_class(reference.name)

    def search_variable(self, name):
        for env in reversed(self.stack):
            if env.has_variable(name):
                return env.get_variable(name)
        raise UndeclaredVariableException(name)

    def search_function(self, name):
        for env in reversed(self.stack):
            if env.has_function(name):
                return env.get_function(name)
        raise UndeclaredFunctionException

    def search_type(self, name):
        for env in reversed(self.stack):
            if env.has_type(name):
                return env.get_type(name)
        raise UndeclaredTypeException
