from constructs import FunctionReference
from symboltable import SymbolTable, BlockScope, GlobalScope


class Visitor:
    def visit(self, name, object):
        getattr(self, name, self.__default__)(object)

    def __default__(self, object):
        pass


class NameResolver(Visitor):
    def __init__(self):
        self.namespace_ = None
        self.table = SymbolTable()

    def __default__(self, construct):
        for child in construct.children:
            print(f'visiting: {child}')
            child.accept(self)

    def namespace(self, namespace):
        self.namespace_ = namespace
        self.table.push(GlobalScope(self.namespace_))

    def function_declaration(self, function):
        self.table.declare_function(function.reference)
        for child in (x for x in function.children if not isinstance(x, FunctionReference)):
            print(f"visiting: {child}")
            child.accept(self)

    def block(self, block):
        self.table.push(BlockScope(self.namespace_))
        self.__default__(block)
        self.table.pop()

    def variable_declaration(self, declaration):
        self.table.declare_variable(declaration.reference)

    def class_declaration(self, declaration):
        self.table.declare_class(declaration.reference)

    def variable_ref(self, ref):
        ref.set_target(self.table.search_variable(ref.name))
        print(ref.target.get_identifier())
