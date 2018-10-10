from lark import Tree


class Construct(Tree):
    construct_name = None

    def __init__(self, children):
        super().__init__(self.construct_name, children)

    def accept(self, visitor):
        visitor.visit(self.construct_name, self)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


class Start(Construct):
    construct_name = "start"


class Namespace(Construct):
    construct_name = "namespace"

    def __init__(self, reference):
        super().__init__([reference])
        self.reference = reference
        self.namespace_path = None

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.reference}'>"


class FunctionDeclaration(Construct):
    construct_name = "function_declaration"

    def __init__(self, reference, arguments, event, expression):
        super().__init__([x for x in [reference, arguments, expression] if x is not None])
        self.reference = reference
        self.arguments = arguments
        self.event = event
        self.expression = expression

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.reference}'>"


class VariableDeclaration(Construct):
    construct_name = "variable_declaration"

    def __init__(self, type, reference, expression):
        super().__init__([x for x in [type, reference, expression] if x is not None])
        self.type = type
        self.reference = reference
        self.expression = expression

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.reference}'>"


class Statement(Construct):
    construct_name = "statement"
    pass


class ExpressionStatement(Statement):
    construct_name = "expression_statement"

    def __init__(self, expression):
        super().__init__([expression])
        self.expression = expression


class ReturnStatement(ExpressionStatement):
    construct_name = "return_statement"


class Block(Statement):
    construct_name = "block"

    def __init__(self, statements):
        super().__init__(statements)
        self.statements = statements


class Expression(Construct):
    construct_name = "expression"

    def __init__(self, children):
        super().__init__(children)
        self.type = None


class Assignment(Expression):
    construct_name = "assignment"

    def __init__(self, ref, expression):
        super().__init__([ref, expression])
        self.ref = ref
        self.expression = expression


class TwoSidedOperation(Expression):
    construct_name = "two_sided_operation"

    def __init__(self, left_expression, right_expression):
        super().__init__([left_expression, right_expression])
        self.left_expression = left_expression
        self.right_expression = right_expression


class UnaryOperation(Expression):
    construct_name = "unary_operation"

    def __init__(self, expression):
        super().__init__([expression])
        self.expression = expression


class OrOperation(TwoSidedOperation):
    construct_name = "or_operation"


class AndOperation(TwoSidedOperation):
    construct_name = "and_operation"


class EqualityOperation(TwoSidedOperation):
    construct_name = "equality_operation"


class UnequalityOperation(TwoSidedOperation):
    construct_name = "unequality_operation"


class LessThenOperation(TwoSidedOperation):
    construct_name = "less_then_operation"


class LessThenEqualsOperation(TwoSidedOperation):
    construct_name = "less_then_equals_operation"


class GreaterThenOperation(TwoSidedOperation):
    construct_name = "greater_then_operation"


class GreaterThenEqualsOperation(TwoSidedOperation):
    construct_name = "greater_then_equals_operation"


class AdditionOperation(TwoSidedOperation):
    construct_name = "addition_operation"


class SubtractionOperation(TwoSidedOperation):
    construct_name = "subtraction_operation"


class MultiplicationOperation(TwoSidedOperation):
    construct_name = "multiplication_operation"


class DivisionOperation(TwoSidedOperation):
    construct_name = "division_operation"


class UnaryPlusOperation(UnaryOperation):
    construct_name = "unary_plus_operation"


class UnaryMinusOperation(UnaryOperation):
    construct_name = "unary_minus_operation"


class UnaryNotOperation(UnaryOperation):
    construct_name = "unary_not_operation"


class RunExpression(Expression):
    construct_name = "run_expression"

    def __init__(self, command):
        super().__init__([])
        self.command = command

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.command}'>"


class Constant(Expression):
    construct_name = "constant"

    def __init__(self, value):
        super().__init__([])
        self.value = value
        if value.type == "INT":
            self.type = intType
        elif value.type == "BOOLEAN":
            self.type = booleanType
        else:
            assert False

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.value}'>"


class Reference(Construct):
    construct_name = "ref"

    def __init__(self, name):
        super().__init__([])
        self.name = name
        self.target = None

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"


class TypeReference(Reference):
    construct_name = "type_ref"

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.name == other.name


class FunctionReference(Reference):
    construct_name = "function_ref"


class VariableReference(Reference, Expression):
    construct_name = "variable_ref"

    def __init__(self, name):
        Reference.__init__(self, name)
        Expression.__init__(self, [])


class NamespaceReference(Reference):
    construct_name = "namespace_ref"


intType = TypeReference("int")
booleanType = TypeReference("boolean")
