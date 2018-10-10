from constructs import FunctionReference
from exception import TypeMissmatchException, BadOperandException
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
            child.accept(self)

    def namespace(self, namespace):
        self.namespace_ = namespace
        self.table.push(GlobalScope(self.namespace_))

    def function_declaration(self, function):
        self.table.declare_function(function.reference)
        for child in (x for x in function.children if not isinstance(x, FunctionReference)):
            child.accept(self)

    def block(self, block):
        self.table.push(BlockScope(self.namespace_))
        self.__default__(block)
        self.table.pop()

    def variable_declaration(self, declaration):
        declaration.type_ref.accept(self)
        self.table.declare_variable(declaration.reference, declaration.type_ref.type)
        declaration.reference.accept(self)
        if declaration.expression is not None:
            declaration.expression.accept(self)

    def class_declaration(self, declaration):
        self.table.declare_class(declaration.reference)

    def type_ref(self, ref):
        ref.type = self.table.search_type(ref.name)

    def variable_ref(self, ref):
        ref.target = self.table.search_variable(ref.name)
        ref.type = ref.target.type

    def assignment(self, assignment):
        self.__default__(assignment)
        if assignment.ref.type != assignment.expression.type:
            raise BadOperandException("=", assignment.ref.type, assignment.expression.type)
        assignment.type = assignment.ref.type

    def or_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.booleanType or expression.right_expression.type != GlobalScope.booleanType:
            raise BadOperandException("||", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.booleanType

    def and_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.booleanType or expression.right_expression.type != GlobalScope.booleanType:
            raise BadOperandException("&&", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.booleanType

    def equality_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != expression.right_expression.type:
            raise BadOperandException("==", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.booleanType

    def unequality_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != expression.right_expression.type:
            raise BadOperandException("!=", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.booleanType

    def less_then_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.intType or expression.right_expression.type != GlobalScope.intType:
            raise BadOperandException("<", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.booleanType

    def less_then_equals_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.intType or expression.right_expression.type != GlobalScope.intType:
            raise BadOperandException("<=", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.booleanType

    def greater_then_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.intType or expression.right_expression.type != GlobalScope.intType:
            raise BadOperandException(">", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.booleanType

    def greater_then_equals_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.intType or expression.right_expression.type != GlobalScope.intType:
            raise BadOperandException(">=", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.booleanType

    def addition_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.intType or expression.right_expression.type != GlobalScope.intType:
            raise BadOperandException("+", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.intType

    def subtraction_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.intType or expression.right_expression.type != GlobalScope.intType:
            raise BadOperandException("-", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.intType

    def multiplication_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.intType or expression.right_expression.type != GlobalScope.intType:
            raise BadOperandException("*", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.intType

    def division_operation(self, expression):
        self.__default__(expression)
        if expression.left_expression.type != GlobalScope.intType or expression.right_expression.type != GlobalScope.intType:
            raise BadOperandException("/", expression.left_expression.type, expression.right_expression.type)
        expression.type = GlobalScope.intType

    def unary_plus_operation(self, expression):
        if expression.expression.type != GlobalScope.intType:
            raise BadOperandException("+", expression.expression.type)
        expression.type = GlobalScope.intType

    def unary_minus_operation(self, expression):
        if expression.expression.type != GlobalScope.intType:
            raise BadOperandException("-", expression.expression.type)
        expression.type = GlobalScope.intType

    def unary_not_operation(self, expression):
        if expression.expression.type != GlobalScope.booleanType:
            raise BadOperandException("!", expression.expression.type)
        expression.type = GlobalScope.booleanType
