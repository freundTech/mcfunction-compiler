from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type

from lark import Tree

from helper import Singleton
from symboltable import IntType, BooleanType

if TYPE_CHECKING:
    from typing import List, Any
    from lark.lexer import Token
    from instructions import Instruction
    from visitor import Visitor


class Construct(Tree):
    construct_name: str = None

    def __init__(self, children: List[Construct]):
        super().__init__(self.construct_name, children)
        self.code: List[Instruction] = None

    def accept(self, visitor: Visitor):
        visitor.visit(self.construct_name, self)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class Start(Construct):
    construct_name: str = "start"


class Namespace(Construct):
    construct_name: str = "namespace"

    def __init__(self, reference: NamespaceReference):
        super().__init__([reference])
        self.reference: NamespaceReference = reference
        self.name: str = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.reference}'>"


class McfcNamespace(Namespace, metaclass=Singleton):
    def __init__(self):
        super().__init__(None)
        self.name = "mcfc"


class ArgumentsDeclaration(Construct):
    construct_name: str = "arguments"

    def __init__(self, arguments: List[ArgumentDeclaration]):
        super().__init__(arguments)
        self.arguments = arguments


class ArgumentDeclaration(Construct):
    construct_name: str = "argument"

    def __init__(self, type_: TypeReference, reference: VariableReference):
        super().__init__([type_, reference])
        self.type: TypeReference = type
        self.reference: VariableReference = reference


class Events(Construct):
    construct_name: str = "events"

    def __init__(self, events):
        super().__init__(events)
        self.events = events


class Event(Construct):
    construct_name: str = "event"

    def __init__(self, namespace: NamespaceReference, function_: FunctionReference):
        super().__init__([namespace, function_])
        self.namespace: NamespaceReference = namespace
        self.function: FunctionReference = function_

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.namespace}:{self.function}'"


class FunctionDeclaration(Construct):
    construct_name: str = "function_declaration"

    def __init__(self, reference: FunctionReference, arguments: ArgumentsDeclaration, event: Event, block: Block):
        super().__init__([x for x in [reference, arguments, block] if x is not None])
        self.reference: FunctionReference = reference
        self.arguments: ArgumentsDeclaration = arguments
        self.event: Event = event
        self.block: Block = block

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.reference}'>"


class Statement(Construct):
    construct_name: str = "statement"


class VariableDeclaration(Statement):
    construct_name: str = "variable_declaration"

    def __init__(self, type_ref: TypeReference, reference: VariableReference, expression: Optional[Expression] = None):
        super().__init__([x for x in [type_ref, reference, expression] if x is not None])
        self.type_ref: TypeReference = type_ref
        self.reference: VariableReference = reference
        self.expression: Expression = expression
        self.type: Type = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.reference}'>"


class ExpressionStatement(Statement):
    construct_name: str = "expression_statement"

    def __init__(self, expression: Expression):
        super().__init__([expression])
        self.expression: Expression = expression


class ReturnStatement(ExpressionStatement):
    construct_name: str = "return_statement"


class Block(Statement):
    construct_name: str = "block"

    def __init__(self, statements: List[Statement]):
        super().__init__(statements)
        self.statements: List[Statement] = statements


class Expression(Construct):
    construct_name: str = "expression"

    def __init__(self, children: List[Expression]):
        super().__init__(children)
        self.type: Type = None


class Assignment(Expression):
    construct_name: str = "assignment"

    def __init__(self, ref: VariableReference, expression: Expression):
        super().__init__([ref, expression])
        self.ref: VariableReference = ref
        self.expression: Expression = expression


class TwoSidedOperation(Expression):
    construct_name: str = "two_sided_operation"

    def __init__(self, left_expression: Expression, right_expression: Expression):
        super().__init__([left_expression, right_expression])
        self.left_expression: Expression = left_expression
        self.right_expression: Expression = right_expression


class UnaryOperation(Expression):
    construct_name: str = "unary_operation"

    def __init__(self, expression: Expression):
        super().__init__([expression])
        self.expression: Expression = expression


class OrOperation(TwoSidedOperation):
    construct_name: str = "or_operation"


class AndOperation(TwoSidedOperation):
    construct_name: str = "and_operation"


class EqualityOperation(TwoSidedOperation):
    construct_name: str = "equality_operation"


class UnequalityOperation(TwoSidedOperation):
    construct_name: str = "unequality_operation"


class LessThenOperation(TwoSidedOperation):
    construct_name: str = "less_then_operation"


class LessThenEqualsOperation(TwoSidedOperation):
    construct_name: str = "less_then_equals_operation"


class GreaterThenOperation(TwoSidedOperation):
    construct_name: str = "greater_then_operation"


class GreaterThenEqualsOperation(TwoSidedOperation):
    construct_name: str = "greater_then_equals_operation"


class AdditionOperation(TwoSidedOperation):
    construct_name: str = "addition_operation"


class SubtractionOperation(TwoSidedOperation):
    construct_name: str = "subtraction_operation"


class MultiplicationOperation(TwoSidedOperation):
    construct_name: str = "multiplication_operation"


class DivisionOperation(TwoSidedOperation):
    construct_name: str = "division_operation"


class ModuloOperation(TwoSidedOperation):
    construct_name: str = "modulo_operation"


class UnaryPlusOperation(UnaryOperation):
    construct_name: str = "unary_plus_operation"


class UnaryMinusOperation(UnaryOperation):
    construct_name: str = "unary_minus_operation"


class UnaryNotOperation(UnaryOperation):
    construct_name: str = "unary_not_operation"


class RunExpression(Expression):
    construct_name: str = "run_expression"

    # TODO: Use String type instead of token
    def __init__(self, command: Token):
        super().__init__([])
        self.command: Token = command[1:-1].encode("utf-8").decode("unicode_escape")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.command}'>"


class Constant(Expression):
    construct_name: str = "constant"

    def __init__(self, value: Token):
        super().__init__([])
        self.value: Token = value
        self.type: Type = None
        if value.type == "INT":
            self.type = IntType()
        elif value.type == "BOOLEAN":
            self.type = BooleanType()
        else:
            assert False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.value}'>"


class Reference(Construct):
    construct_name: str = "ref"

    def __init__(self, name: Token):
        super().__init__([])
        self.name: Token = name
        self.target: Any = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.name}'>"


class TypeReference(Reference):
    construct_name: str = "type_ref"

    def __init__(self, name):
        super().__init__(name)
        self.type: Type = None


class FunctionReference(Reference):
    construct_name: str = "function_ref"


class VariableReference(Reference, Expression):
    construct_name: str = "variable_ref"

    def __init__(self, name: Token):
        Reference.__init__(self, name)
        Expression.__init__(self, [])


class NamespaceReference(Reference):
    construct_name: str = "namespace_ref"
