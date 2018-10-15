import unittest

from lark import Lark, Tree, ParseError, UnexpectedCharacters
from lark.lexer import Token
from pkg_resources import resource_string, resource_filename


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.grammar = resource_string("resources", "grammar.lark").decode()

    def testNamespace(self):
        l = Lark(self.grammar, parser="earley", start="namespace")
        t = l.parse("namespace test;")
        self.assertEqual(t, Tree("namespace", [
            Tree("namespace_ref", [
                Token("IDENTIFIER", "test")
            ])
        ]))

    def testVariableDeclarations(self):
        l = Lark(self.grammar, parser="earley", start="variable_declaration")
        self.assertEqual(l.parse("int test;"),
                         Tree("variable_declaration", [
                             Tree("type_ref", [
                                 Token("IDENTIFIER", "int")
                             ]),
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ])
                         ])
                         )
        self.assertEqual(l.parse("boolean test;"),
                         Tree("variable_declaration", [
                             Tree("type_ref", [
                                 Token("IDENTIFIER", "boolean")
                             ]),
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ])
                         ])
                         )
        self.assertEqual(l.parse("int test = 0;"),
                         Tree("variable_declaration", [
                             Tree("type_ref", [
                                 Token("IDENTIFIER", "int")
                             ]),
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "0")
                             ])
                         ])
                         )
        # Missing semicolon
        self.assertRaises(ParseError, lambda: l.parse("int test"))
        # Missing type
        self.assertRaises(UnexpectedCharacters, lambda: l.parse("test = 0;"))

    def testExpression(self):
        l = Lark(self.grammar, parser="earley", start="expression")
        self.assertEqual(l.parse("test = 1"),
                         Tree("assignment", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", 1)
                             ])
                         ]))
        self.assertEqual(l.parse("test || true"),
                         Tree("or_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("BOOLEAN", "true")
                             ])
                         ]))
        self.assertEqual(l.parse("test && true"),
                         Tree("and_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("BOOLEAN", "true")
                             ])
                         ]))
        self.assertEqual(l.parse("test == true"),
                         Tree("equality_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("BOOLEAN", "true")
                             ])
                         ]))
        self.assertEqual(l.parse("test != true"),
                         Tree("unequality_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("BOOLEAN", "true")
                             ])
                         ]))
        self.assertEqual(l.parse("test < 1"),
                         Tree("less_then_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("test <= 1"),
                         Tree("less_then_equals_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("test > 1"),
                         Tree("greater_then_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("test >= 1"),
                         Tree("greater_then_equals_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("test + 1"),
                         Tree("addition_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("test - 1"),
                         Tree("subtraction_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("test * 1"),
                         Tree("multiplication_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("test / 1"),
                         Tree("division_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("test % 1"),
                         Tree("modulo_operation", [
                             Tree("variable_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("+1"),
                         Tree("unary_plus_operation", [
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("-1"),
                         Tree("unary_minus_operation", [
                             Tree("constant", [
                                 Token("INT", "1")
                             ])
                         ]))
        self.assertEqual(l.parse("!true"),
                         Tree("unary_not_operation", [
                             Tree("constant", [
                                 Token("BOOLEAN", "true")
                             ])
                         ]))
        self.assertEqual(l.parse("(1 + 2) * 3"),
                         Tree("multiplication_operation", [
                             Tree("addition_operation", [
                                 Tree("constant", [
                                     Token("INT", "1")
                                 ]),
                                 Tree("constant", [
                                     Token("INT", "2")
                                 ])
                             ]),
                             Tree("constant", [
                                 Token("INT", "3")
                             ])
                         ]))
        self.assertEqual(l.parse("test(1, 2)"),
                         Tree("call", [
                             Tree("function_ref", [
                                 Token("IDENTIFIER", "test")
                             ]),
                             Tree("arguments", [
                                 Tree("constant", [
                                     Token("INT", "1")
                                 ]),
                                 Tree("constant", [
                                     Token("INT", 2)
                                 ])
                             ])
                         ]))
        self.assertEqual(l.parse(
            "test || (test2 = true) && test3 == !test4 != test5 < test6 <= test7 > test8 >= test9 + +1 - 2 * -3 / test10(4)"),
            Tree("or_operation", [
                Tree("variable_ref", [
                    Token("IDENTIFIER", "test")
                ]),
                Tree("and_operation", [
                    Tree("assignment", [
                        Tree("variable_ref", [
                            Token("IDENTIFIER", "test2")
                        ]),
                        Tree("constant", [
                            Token("BOOLEAN", "true")
                        ])
                    ]),
                    Tree("unequality_operation", [
                        Tree("equality_operation", [
                            Tree("variable_ref", [
                                Token("IDENTIFIER", "test3")
                            ]),
                            Tree("unary_not_operation", [
                                Tree("variable_ref", [
                                    Token("IDENTIFIER", "test4")
                                ])
                            ])
                        ]),
                        Tree("greater_then_equals_operation", [
                            Tree("greater_then_operation", [
                                Tree("less_then_equals_operation", [
                                    Tree("less_then_operation", [
                                        Tree("variable_ref", [
                                            Token("IDENTIFIER", "test5")
                                        ]),
                                        Tree("variable_ref", [
                                            Token("IDENTIFIER", "test6")
                                        ])
                                    ]),
                                    Tree("variable_ref", [
                                        Token("IDENTIFIER", "test7")
                                    ])
                                ]),
                                Tree("variable_ref", [
                                    Token("IDENTIFIER", "test8")
                                ]),
                            ]),
                            Tree("subtraction_operation", [
                                Tree("addition_operation", [
                                    Tree("variable_ref", [
                                        Token("IDENTIFIER", "test9")
                                    ]),
                                    Tree("unary_plus_operation", [
                                        Tree("constant", [
                                            Token("INT", "1")
                                        ])
                                    ])
                                ]),
                                Tree("division_operation", [
                                    Tree("multiplication_operation", [
                                        Tree("constant", [
                                            Token("INT", "2")
                                        ]),
                                        Tree("unary_minus_operation", [
                                            Tree("constant", [
                                                Token("INT", "3")
                                            ])
                                        ]),
                                    ]),
                                    Tree("call", [
                                        Tree("function_ref", [
                                            Token("IDENTIFIER", "test10")
                                        ]),
                                        Tree("arguments", [
                                            Tree("constant", [
                                                Token("INT", "4")
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ])
                ])
            ]))


if __name__ == '__main__':
    unittest.main()
