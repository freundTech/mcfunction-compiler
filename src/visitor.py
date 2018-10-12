from typing import Any

from constructs import FunctionReference, Namespace, Construct, FunctionDeclaration, Block, VariableDeclaration, \
    TypeReference, VariableReference, Assignment, Expression, OrOperation, AndOperation, EqualityOperation, \
    UnequalityOperation, LessThenOperation, LessThenEqualsOperation, GreaterThenOperation, GreaterThenEqualsOperation, \
    AdditionOperation, SubtractionOperation, MultiplicationOperation, DivisionOperation, UnaryPlusOperation, \
    UnaryMinusOperation, UnaryNotOperation
from exception import BadOperandException
from symboltable import SymbolTable, BlockScope, GlobalScope, BooleanType, IntType


class Visitor:
    def visit(self, name: str, object_: Any):
        getattr(self, name, self.__default__)(object_)

    def __default__(self, object):
        pass


class NameResolver(Visitor):
    def __init__(self):
        self.namespace_: Namespace = None
        self.table: SymbolTable = SymbolTable()

    def __default__(self, construct: Construct):
        for child in construct.children:
            child.accept(self)

    def namespace(self, namespace: Namespace):
        self.namespace_ = namespace
        self.table.push(GlobalScope(self.namespace_))

    def function_declaration(self, function_: FunctionDeclaration):
        self.table.declare_function(function_.reference)
        for child in (x for x in function_.children if not isinstance(x, FunctionReference)):
            child.accept(self)

    def block(self, block: Block):
        self.table.push(BlockScope(self.namespace_))
        self.__default__(block)
        self.table.pop()

    def variable_declaration(self, declaration: VariableDeclaration):
        declaration.type_ref.accept(self)
        self.table.declare_variable(declaration.reference, declaration.type_ref.type)
        declaration.reference.accept(self)
        if declaration.expression is not None:
            declaration.expression.accept(self)

    #def class_declaration(self, declaration: ClassDeclaration):
    #    self.table.declare_class(declaration.reference)

    def type_ref(self, ref: TypeReference):
        ref.type = self.table.search_type(ref.name)

    def variable_ref(self, ref: VariableReference):
        ref.target = self.table.search_variable(ref.name)
        ref.type = ref.target.type

    def assignment(self, assignment: Assignment):
        self.__default__(assignment)
        if assignment.ref.type != assignment.expression.type:
            raise BadOperandException("=", assignment.ref.type, assignment.expression.type)
        assignment.type = assignment.ref.type

    def or_operation(self, expression: OrOperation):
        self.__default__(expression)
        if expression.left_expression.type != BooleanType.get_instance() or expression.right_expression.type != BooleanType.get_instance():
            raise BadOperandException("||", expression.left_expression.type, expression.right_expression.type)
        expression.type = BooleanType.get_instance()

    def and_operation(self, expression: AndOperation):
        self.__default__(expression)
        if expression.left_expression.type != BooleanType.get_instance() or expression.right_expression.type != BooleanType.get_instance():
            raise BadOperandException("&&", expression.left_expression.type, expression.right_expression.type)
        expression.type = BooleanType.get_instance()

    def equality_operation(self, expression: EqualityOperation):
        self.__default__(expression)
        if expression.left_expression.type != expression.right_expression.type:
            raise BadOperandException("==", expression.left_expression.type, expression.right_expression.type)
        expression.type = BooleanType.get_instance()

    def unequality_operation(self, expression: UnequalityOperation):
        self.__default__(expression)
        if expression.left_expression.type != expression.right_expression.type:
            raise BadOperandException("!=", expression.left_expression.type, expression.right_expression.type)
        expression.type = BooleanType.get_instance()

    def less_then_operation(self, expression: LessThenOperation):
        self.__default__(expression)
        if expression.left_expression.type != IntType.get_instance() or expression.right_expression.type != IntType.get_instance():
            raise BadOperandException("<", expression.left_expression.type, expression.right_expression.type)
        expression.type = BooleanType.get_instance()

    def less_then_equals_operation(self, expression: LessThenEqualsOperation):
        self.__default__(expression)
        if expression.left_expression.type != IntType.get_instance() or expression.right_expression.type != IntType.get_instance():
            raise BadOperandException("<=", expression.left_expression.type, expression.right_expression.type)
        expression.type = BooleanType.get_instance()

    def greater_then_operation(self, expression: GreaterThenOperation):
        self.__default__(expression)
        if expression.left_expression.type != IntType.get_instance() or expression.right_expression.type != IntType.get_instance():
            raise BadOperandException(">", expression.left_expression.type, expression.right_expression.type)
        expression.type = BooleanType.get_instance()

    def greater_then_equals_operation(self, expression: GreaterThenEqualsOperation):
        self.__default__(expression)
        if expression.left_expression.type != IntType.get_instance() or expression.right_expression.type != IntType.get_instance():
            raise BadOperandException(">=", expression.left_expression.type, expression.right_expression.type)
        expression.type = BooleanType.get_instance()

    def addition_operation(self, expression: AdditionOperation):
        self.__default__(expression)
        if expression.left_expression.type != IntType.get_instance() or expression.right_expression.type != IntType.get_instance():
            raise BadOperandException("+", expression.left_expression.type, expression.right_expression.type)
        expression.type = IntType.get_instance()

    def subtraction_operation(self, expression: SubtractionOperation):
        self.__default__(expression)
        if expression.left_expression.type != IntType.get_instance() or expression.right_expression.type != IntType.get_instance():
            raise BadOperandException("-", expression.left_expression.type, expression.right_expression.type)
        expression.type = IntType.get_instance()

    def multiplication_operation(self, expression: MultiplicationOperation):
        self.__default__(expression)
        if expression.left_expression.type != IntType.get_instance() or expression.right_expression.type != IntType.get_instance():
            raise BadOperandException("*", expression.left_expression.type, expression.right_expression.type)
        expression.type = IntType.get_instance()

    def division_operation(self, expression: DivisionOperation):
        self.__default__(expression)
        if expression.left_expression.type != IntType.get_instance() or expression.right_expression.type != IntType.get_instance():
            raise BadOperandException("/", expression.left_expression.type, expression.right_expression.type)
        expression.type = IntType.get_instance()

    def unary_plus_operation(self, expression: UnaryPlusOperation):
        if expression.expression.type != IntType.get_instance():
            raise BadOperandException("+", expression.expression.type)
        expression.type = IntType.get_instance()

    def unary_minus_operation(self, expression: UnaryMinusOperation):
        if expression.expression.type != IntType.get_instance():
            raise BadOperandException("-", expression.expression.type)
        expression.type = IntType.get_instance()

    def unary_not_operation(self, expression: UnaryNotOperation):
        if expression.expression.type != BooleanType.get_instance():
            raise BadOperandException("!", expression.expression.type)
        expression.type = BooleanType.get_instance()
