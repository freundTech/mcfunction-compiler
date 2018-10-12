from __future__ import annotations

from typing import List, Dict, Optional

from constructs import FunctionDeclaration, Block, Arguments, Constant, VariableDeclaration, Namespace, Start, \
    Construct, ExpressionStatement, RunExpression, Assignment, AdditionOperation, VariableReference, OrOperation, \
    EqualityOperation
from instructions import StoreInstruction, RunInstruction, \
    AdditionInstruction, CallInstruction, EqualityInstruction, IfNotInstruction, Instruction
from symboltable import BuiltinType, BlockScope, Scope
from visitor import Visitor


class NameManager:
    def __init__(self, namespace: Namespace):
        self.registers: List[Scope.Variable] = []
        self.function_count: int = 0
        self.namespace: Namespace = namespace

    def create_register(self, type_: Scope.Type):
        self.registers.append(BlockScope.LocalVariable(self.namespace, f"r{len(self.registers)}", type_))
        return self.registers[-1]

    def get_register(self, index: int=0):
        return self.registers[-1 - index]

    def free_register(self):
        self.registers.pop()

    def create_function(self):
        self.function_count += 1
        return f"{self.function_count}"


class CodeGenerator(Visitor):
    def __init__(self):
        self.namespace_: Namespace = None
        self.functions: Dict[List[Instruction]] = {}
        self.variables: set = set()
        self.events: Dict = {}
        self.name_manager: Optional[NameManager] = None

    def __default__(self, construct: Construct):
        raise Exception(construct)

    def start(self, start: Start):
        start.code = []
        for child in start.children:
            child.accept(self)
            start.code += child.code
        self.functions["init"] = start.code
        for function in self.functions:
            print(f"{function.upper()}:")
            for instruction in self.functions[function]:
                print(instruction.to_string())

    def namespace(self, namespace: Namespace):
        self.namespace_ = namespace.reference.name
        self.name_manager = NameManager(namespace)
        namespace.code = []

    def variable_declaration(self, declaration: VariableDeclaration):
        if isinstance(declaration.type_ref.type, BuiltinType):
            self.variables.add(declaration.reference.name)
        else:
            raise NotImplementedError
        if declaration.expression is not None:
            declaration.expression.accept(self)
            declaration.code = declaration.expression.code
            declaration.code.append(StoreInstruction(declaration.reference.target, self.name_manager.get_register()))
            self.name_manager.free_register()
        else:
            declaration.code = []

    def constant(self, constant: Constant):
        constant.code = [StoreInstruction(self.name_manager.create_register(constant.type), constant)]

    def arguments(self, arguments: Arguments):
        arguments.code = []
        for child in arguments.children:
            child.accept(self)
            arguments.code += child.code

    def function_declaration(self, declaration: FunctionDeclaration):
        declaration.arguments.accept(self)
        declaration.block.accept(self)
        code = declaration.arguments.code + declaration.block.code
        self.functions[declaration.reference.name] = code
        declaration.code = []

    def block(self, block: Block):
        block.code = []
        for statement in block.statements:
            statement.accept(self)
            block.code += statement.code

    def expression_statement(self, statement: ExpressionStatement):
        statement.expression.accept(self)
        statement.code = statement.expression.code

    def run_expression(self, expression: RunExpression):
        expression.code = [RunInstruction(expression.command)]

    def assignment(self, assignment: Assignment):
        assignment.expression.accept(self)
        assignment.code = assignment.expression.code
        assignment.code.append(StoreInstruction(assignment.ref.target, self.name_manager.get_register()))
        self.name_manager.free_register()

    def or_operation(self, operation: OrOperation):
        operation.left_expression.accept(self)
        operation.right_expression.accept(self)
        function_name = self.name_manager.create_function()
        operation.code = operation.left_expression.code + [IfNotInstruction(self.name_manager.get_register(), CallInstruction(self.namespace_, function_name))]
        self.functions[function_name] = operation.right_expression.code
        self.name_manager.free_register()

    def equality_operation(self, operation: EqualityOperation):
        operation.left_expression.accept(self)
        operation.right_expression.accept(self)
        operation.code = operation.left_expression.code + operation.right_expression.code + [EqualityInstruction(self.name_manager.get_register(1), self.name_manager.get_register())]
        self.name_manager.free_register()

    def addition_operation(self, operation: AdditionOperation):
        operation.left_expression.accept(self)
        operation.right_expression.accept(self)
        operation.code = operation.left_expression.code + operation.right_expression.code + [AdditionInstruction(self.name_manager.get_register(1), self.name_manager.get_register())]
        self.name_manager.free_register()

    def variable_ref(self, reference: VariableReference):
        reference.code = [StoreInstruction(self.name_manager.create_register(reference.type), reference.target)]
