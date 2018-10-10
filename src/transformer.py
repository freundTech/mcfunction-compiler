from lark import Transformer
from lark.lexer import Token

from constructs import *


def token_to_int(token):
    return Token.new_borrow_pos(token.type, int(token), token)


def token_to_boolean(token):
    return Token.new_borrow_pos(token.type, token == "true", token)


def token_to_string(token):
    return Token.new_borrow_pos(token.type, token[1:-1].encode("utf-8").decode("unicode_escape"), token)


class TreeTransformer(Transformer):
    def start(self, args):
        return Start(args)

    def namespace(self, args):
        return Namespace(args[0])

    def arguments(self, args):
        raise NotImplementedError

    def function_declaration(self, args):
        arguments = None
        event = None
        for arg in args[1:-1]:
            if arg.data == "arguments":
                arguments = arg
            elif arg.data == "event":
                event = arg
        return FunctionDeclaration(args[0], arguments, event, args[-1])

    def variable_declaration(self, args):
        if len(args) > 2:
            return VariableDeclaration(args[0], args[1], args[2])
        else:
            return VariableDeclaration(args[0], args[1], None)

    def class_declaration(self, args):
        raise NotImplementedError

    def class_body(self, args):
        raise NotImplementedError

    def block(self, args):
        return Block(args)

    def expression_statement(self, args):
        return ExpressionStatement(args[0])

    def return_statement(self, args):
        return ReturnStatement(args[0])

    def assignment(self, args):
        return Assignment(args[0], args[1])

    def or_operation(self, args):
        return OrOperation(args[0], args[1])

    def and_operation(self, args):
        return AndOperation(args[0], args[1])

    def equality_operation(self, args):
        return EqualityOperation(args[0], args[1])

    def unequality_operation(self, args):
        return UnequalityOperation(args[0], args[1])

    def less_then_operation(self, args):
        return LessThenOperation(args[0], args[1])

    def less_then_equals_operation(self, args):
        return LessThenEqualsOperation(args[0], args[1])

    def greater_then_operation(self, args):
        return GreaterThenOperation(args[0], args[1])

    def greater_then_equals_operation(self, args):
        return GreaterThenEqualsOperation(args[0], args[1])

    def addition_operation(self, args):
        return AdditionOperation(args[0], args[1])

    def subtraction_operation(self, args):
        return SubtractionOperation(args[0], args[1])

    def multiplication_operation(self, args):
        return MultiplicationOperation(args[0], args[1])

    def division_operation(self, args):
        return DivisionOperation(args[0], args[1])

    def unary_plus_operation(self, args):
        return UnaryPlusOperation(args[0])

    def unary_minus_operation(self, args):
        return UnaryMinusOperation(args[0])

    def unary_not_operation(self, args):
        return UnaryNotOperation(args[0])

    def run_expression(self, args):
        return RunExpression(args[0])

    def type_ref(self, args):
        return TypeReference(args[0])

    def function_ref(self, args):
        return FunctionReference(args[0])

    def variable_ref(self, args):
        return VariableReference(args[0])

    def namespace_ref(self, args):
        return NamespaceReference(args[0])

    def constant(self, args):
        return Constant(args[0])
