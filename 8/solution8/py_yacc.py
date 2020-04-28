#! /usr/bin/env python
# coding=utf-8
import ply.yacc as yacc
from py_lex import *
from node import node, num_node


# YACC for parsing Python

def simple_node(t, name):
    t[0] = node(name)
    for i in range(1, len(t)):
        t[0].add(node(t[i]))
    return t[0]


def p_program(t):
    '''program : statements'''
    if len(t) == 2:
        t[0] = node('[PROGRAM]')
        t[0].add(t[1])


def p_statements(t):
    '''statements : statements statement
                  | statement'''
    if len(t) == 3:
        t[0] = node('[STATEMENTS]')
        t[0].add(t[1])
        t[0].add(t[2])
    elif len(t) == 2:
        t[0] = node('[STATEMENTS]')
        t[0].add(t[1])


def p_statement(t):
    ''' statement : assignment
                  | operation
                  | print'''
    if len(t) == 2:
        t[0] = node(['STATEMENT'])
        t[0].add(t[1])


def p_assignment(t):
    '''assignment : VARIABLE '=' NUMBER'''
    if len(t) == 4:
        t[0] = node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(num_node(t[3]))


def p_operation(p):
    '''operation : VARIABLE '=' expression'''
    p[0] = node('[OPERATION]')
    p[0].add(node(p[1]))
    p[0].add(node('='))
    p[0].add(p[3])


def p_expression(p):
    '''expression : expression '+' term
                  | expression '-' term
                  | term
    '''
    p[0] = node('[EXPRESSION]')
    if len(p) == 4:
        p[0].add(p[1])
        p[0].add(node(p[2]))
        p[0].add(p[3])
    elif len(p) == 2:
        p[0].add(p[1])


def p_term(p):
    '''term : term '*' factor
            | term '/' factor
            | factor
    '''
    p[0] = node('[TERM]')
    if len(p) == 4:
        p[0].add(p[1])
        p[0].add(node(p[2]))
        p[0].add(p[3])
    elif len(p) == 2:
        p[0].add(p[1])


def p_factor(p):
    '''factor : VARIABLE
              | '(' expression ')'
              | NUMBER
    '''
    p[0] = node('[FACTOR]')
    if len(p) == 2:
        if p[1].isdigit():
            p[0].add(num_node(p[1]))
        else:
            p[0].add(node(p[1]))
    elif len(p) == 4:
        p[0].add(node('('))
        p[0].add(node(p[2]))
        p[0].add(node(')'))


def p_variables(p):
    '''variables : variables ',' VARIABLE
                 | VARIABLE
    '''
    p[0] = node('[VARIABLES]')
    if len(p) == 4:
        p[0].add(p[1])
        p[0].add(node(p[2]))
        p[0].add(node(p[3]))
    elif len(p) == 2:
        p[0].add(node(p[1]))


def p_print(t):
    '''print : PRINT '(' variables ')' '''
    if len(t) == 5:
        t[0] = node('[PRINT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])
        t[0].add(node(t[4]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()
