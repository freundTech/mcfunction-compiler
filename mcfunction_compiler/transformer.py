from __future__ import annotations

from lark import Transformer
from lark.lexer import Token

from constructs import *


class TreeTransformer(Transformer):
    def start(self, args: List[Any]):
        for arg in args:
            assert isinstance(arg, Construct)
        return Start(args)

    def namespace(self, args: List[Any]):
        assert len(args) == 1
        assert isinstance(args[0], NamespaceReference)
        return Namespace(args[0])

    def arguments_declaration(self, args: List[Any]):
        for arg in args:
            assert isinstance(arg, ArgumentDeclaration)
        return ArgumentsDeclaration(args)

    def argument_declaration(self, args: List[Any]):
        assert isinstance(args[0], TypeReference)
        assert isinstance(args[1], VariableReference)
        return ArgumentDeclaration(args[0], args[1])

    def events(self, args: List[Any]):
        for arg in args:
            assert isinstance(arg, Event)
        return Events(args)

    def event(self, args: List[Any]):
        assert isinstance(args[0], NamespaceReference)
        assert isinstance(args[1], FunctionReference)
        return Event(args[0], args[1])

    def function_declaration(self, args: List[Any]):
        assert isinstance(args[0], FunctionReference)
        assert isinstance(args[1], ArgumentsDeclaration)
        assert isinstance(args[2], Events)
        assert isinstance(args[3], Block)
        return FunctionDeclaration(args[0], args[1], args[2], args[3])

    def variable_declaration(self, args: List[Any]):
        assert isinstance(args[0], TypeReference)
        assert isinstance(args[1], VariableReference)
        # TODO: Get rid of this if
        if len(args) > 2:
            assert isinstance(args[2], Expression)
            return VariableDeclaration(args[0], args[1], args[2])
        else:
            return VariableDeclaration(args[0], args[1], None)

    def class_declaration(self, args: List[Any]):
        raise NotImplementedError

    def class_body(self, args: List[Any]):
        raise NotImplementedError

    def block(self, args: List[Any]):
        for arg in args:
            assert isinstance(arg, Statement)
        return Block(args)

    def expression_statement(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        return ExpressionStatement(args[0])

    def return_statement(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        return ReturnStatement(args[0])

    def assignment(self, args: List[Any]):
        assert isinstance(args[0], VariableReference)
        assert isinstance(args[1], Expression)
        return Assignment(args[0], args[1])

    def or_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return OrOperation(args[0], args[1])

    def and_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return AndOperation(args[0], args[1])

    def equality_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return EqualityOperation(args[0], args[1])

    def unequality_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return UnequalityOperation(args[0], args[1])

    def less_then_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return LessThenOperation(args[0], args[1])

    def less_then_equals_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return LessThenEqualsOperation(args[0], args[1])

    def greater_then_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return GreaterThenOperation(args[0], args[1])

    def greater_then_equals_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return GreaterThenEqualsOperation(args[0], args[1])

    def addition_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return AdditionOperation(args[0], args[1])

    def subtraction_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return SubtractionOperation(args[0], args[1])

    def multiplication_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return MultiplicationOperation(args[0], args[1])

    def division_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        assert isinstance(args[1], Expression)
        return DivisionOperation(args[0], args[1])

    def unary_plus_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        return UnaryPlusOperation(args[0])

    def unary_minus_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        return UnaryMinusOperation(args[0])

    def unary_not_operation(self, args: List[Any]):
        assert isinstance(args[0], Expression)
        return UnaryNotOperation(args[0])

    def run_expression(self, args: List[Any]):
        assert isinstance(args[0], Token)
        assert args[0].type == "STRING"
        return RunExpression(args[0])

    def type_ref(self, args: List[Any]):
        assert isinstance(args[0], Token)
        assert args[0].type == "IDENTIFIER"
        return TypeReference(args[0])

    def function_ref(self, args: List[Any]):
        assert isinstance(args[0], Token)
        assert args[0].type == "IDENTIFIER"
        return FunctionReference(args[0])

    def variable_ref(self, args: List[Any]):
        assert isinstance(args[0], Token)
        assert args[0].type == "IDENTIFIER"
        return VariableReference(args[0])

    def namespace_ref(self, args: List[Any]):
        assert isinstance(args[0], Token)
        assert args[0].type == "IDENTIFIER"
        return NamespaceReference(args[0])

    def constant(self, args: List[Any]):
        assert isinstance(args[0], Token)
        assert args[0].type == "INT" or args[0].type == "BOOLEAN"
        return Constant(args[0])
