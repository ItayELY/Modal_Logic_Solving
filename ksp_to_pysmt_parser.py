from pysmt.shortcuts import Symbol, And, Not, is_sat, Implies, Solver
from pysmt.shortcuts import *
from pysmt.typing import *
from translators import *
from pysmt.solvers import z3
from io import StringIO
from pysmt.smtlib.parser import SmtLibParser
from testing import *
from levels import *
import levels_new_form as lnf
import experimetns as ex
from translate_modal_valuation import *
Box_type = FunctionType(BOOL, [BOOL])
Box = Symbol("box", Box_type)

import re

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def parse_expression(expression):
    # Remove whitespaces from the expression
    expression = expression.replace(" ", "")
    expression = '(' + expression + ')'
    # expression = expression.replace("-", '~')
    expression = expression.replace("not", '~')
    expression = expression.replace("and", '&')
    expression = expression.replace("or", '|')
    expression = expression.replace("<=>", '<->')
    expression = expression.replace("ifonlyif", '<->')
    expression = expression.replace("=>", '->')
    expression = expression.replace("imp", '->')
    expression = expression.replace("then", '->')
    expression = expression.replace("dia", '<>')
    # Define the regular expression patterns for different elements
    number_pattern = r'[a-zA-Z]+'
    operator_pattern = r'[\&\|]'
    implies_pattern = r'->'
    iff_pattern = r'<->'
    box_pattern1 = r'\[\]'
    box_pattern2 = r'box'
    box_pattern = f'{box_pattern1}|{box_pattern2}'
    diamond_pattern = r'\<\>'
    unary_operator_pattern = r'[\!|\~]'
    parentheses_pattern = r'\(|\)'
    pattern = f'({iff_pattern}|{diamond_pattern}|{box_pattern}|{implies_pattern}|{number_pattern}|{operator_pattern}|{unary_operator_pattern}|{parentheses_pattern})'

    tokens = re.findall(pattern, expression)
    # tokens = [t[0] for t in tokens]

    # Initialize a stack to keep track of nodes and operators
    stack = []

    for token in tokens:
        if token == ')':
            x = stack.pop()
            if x == '(':
                continue
            x2 = stack.pop()
            if x2 in ['!', '~']:
                x = (Not(x))
                x2 = stack.pop()
                # stack.append(Not(x))
            if x2 in ['[]', 'box']:
                x = (Box(x))
                x2 = stack.pop()
            if x2 in ['<>', 'dia']:
                x = (Box(x))
                x2 = stack.pop()
            if x2 == '(':
                stack.append(x)
                continue

            while x2 in ['&', '|', '->', '<->']:
                x3 = stack.pop()
                if x2 == '&':
                    x = And(x3, x)
                elif x2 == '->':
                    x = Implies(x3, x)
                elif x2 == '<->':
                    x = And(Implies(x3, x), Implies(x, x3))
                else:
                    x = Or(x3, x)
                x2 = stack.pop()
            if len(stack) > 0:
                x5 = stack.pop()
                if x5 in ['!', '~']:
                    stack.append(Not(x))
                    continue
                if x5 in ['[]', 'box']:
                    stack.append(Box(x))
                    continue
                if x5 == '<>':
                    stack.append(Not(Box(Not(x))))
                    continue
                stack.append(x5)
            stack.append(x)
        else:
            if token in ['(', '!', '&', '|', '->', '<->', '[]', 'box', '~', '<>']:
                stack.append(token)
                continue
            if len(stack) > 0:
                x = stack.pop()
            else:
                x = 'no'
            token = Symbol(token)
            while x in ['!', '~', '[]', 'box', '<>']:
                if x in ['!', '~']:
                    token = Not(token)
                elif x in ['[]', 'box']:
                    token = Box(token)
                elif x == '<>':
                    token = Not(Box(Not(token)))
                if len(stack) != 0:
                    x = stack.pop()
                else:
                    x = 'no'
                    break

            if x != 'no':
                stack.append(x)
            stack.append(token)
        # if re.match(number_pattern, token):
        #     # Create a node for numbers
        #     # node = Node(float(token))
        #     node = Symbol(token)
        #     stack.append(node)
        # elif re.match(unary_operator_pattern, token):
        #     # Create a unary operator node
        #     # node = Node(token)
        #     node = Symbol(token)
        #     # if stack:
        #     #     node.right = stack.pop()
        #     # else:
        #     #     raise ValueError("Invalid expression: Unmatched parentheses.")
        #     stack.append(node)
        # elif re.match(operator_pattern, token):
        #     # Create a node for binary operators or parentheses
        #     node = Node(token)
        #     stack.append(node)
        # elif token == ')':
        #     # Process the nodes and operators until the corresponding '(' is found
        #     if stack:
        #         right = stack.pop()
        #         if stack:
        #             operator = stack.pop()
        #             left = stack.pop()
        #             operator.left = left
        #             operator.right = right
        #             stack.append(operator)
        #         else:
        #             raise ValueError("Invalid expression: Unmatched parentheses.")
        #     else:
        #         raise ValueError("Invalid expression: Unmatched parentheses.")

    # Check if there are remaining elements in the stack (e.g., unmatched parentheses)
    if len(stack) > 1:
        raise ValueError("Invalid expression: Unmatched parentheses.")

    # The final element in the stack will be the root of the tree
    return stack.pop()


def tokenize(formula):
    number_pattern = r'\d+(\.\d+)?'
    operator_pattern = r'[\&\|\*/]'
    unary_operator_pattern = r'[\!]'
    parentheses_pattern = r'\(|\)'
    pattern = f'({number_pattern}|{operator_pattern}|{unary_operator_pattern}|{parentheses_pattern})'

    tokens = re.findall(pattern, formula)
    tokens = [t[0] for t in tokens]
    return tokens

def parse_tokens(tokens):
    if tokens[0] == '!':
        if tokens[1] == '(':
            level = 0
            for i in range(2, len(tokens)):
                if tokens[i] == '(':
                    level += 1
                if tokens[i] == ')':
                    if levels == 0:
                        return Not(parse_tokens(tokens[2:i]))
                    else:
                        levels -= 1
        else: return Not(tokens[1])
    else: return Symbol(tokens[0])
# Example usage
# expression = "~((<>p & <>q) -> (<>(p & <>q) | <>(<>p & q) | <>(p & q)))"
# expression = "!55"
# tree = parse_expression(str(expression))
# tree = parse_expression(expression)
# print(tree.serialize())
# Visualize the tree (inorder traversal)
def inorder_traversal(node):
    if node:
        inorder_traversal(node.left)
        print(node.value, end=" ")
        inorder_traversal(node.right)

# inorder_traversal(tree)




# c = 3