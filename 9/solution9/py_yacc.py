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
                  | print
                  | if
                  | while
                  | for
    '''
    if len(t) == 2:
        t[0] = node(['STATEMENT'])
        t[0].add(t[1])


def p_assignment(t):
    '''assignment : VARIABLE '=' NUMBER
                  | VARIABLE '=' VARIABLE
                  | VARIABLE '=' '[' numbers ']'
                  | VARIABLE '=' VARIABLE '[' VARIABLE ']'
                  | VARIABLE '[' VARIABLE ']' '=' VARIABLE
                  | VARIABLE '[' VARIABLE ']' '=' VARIABLE '[' VARIABLE ']'
    '''
    if len(t) == 4:
        t[0]=simple_node(t,'[ASSIGNMENT]')
    elif len(t)==6:
        t[0]=node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(t[4])
        t[0].add(node(t[5]))
    else:
        t[0] = simple_node(t, '[ASSIGNMENT]')


def p_numbers(p):
    '''numbers : numbers ',' NUMBER
               | NUMBER
    '''
    p[0] = node('[NUMBERS]')
    if len(p) == 4:
        p[0].add(p[1])
        p[0].add(node(p[2]))
        p[0].add(num_node(p[3]))
    elif len(p) == 2:
        p[0].add(num_node(p[1]))


def p_operation(p):
    '''operation : VARIABLE '=' expression
                 | VARIABLE '=' LEN '(' VARIABLE ')'
                 | VARIABLE PLUS
    '''
    if len(p) == 4:
        p[0] = node('[OPERATION]')
        p[0].add(node(p[1]))
        p[0].add(node('='))
        p[0].add(p[3])
    elif len(p) == 7:
        p[0] = simple_node(p, '[OPERATION]')
    elif len(p) == 3:
        p[0] = simple_node(p, '[OPERATION]')


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
            | term DIVISION factor
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
        p[0].add(p[2])
        p[0].add(node(')'))


def p_print(t):
    '''print : PRINT '(' VARIABLE ')' '''
    if len(t) == 5:
        t[0] = simple_node(t, '[PRINT]')


def p_if(t):
    r'''if : IF '(' condition ')' '{' statements '}'
           | IF '(' condition ')' '{' statements '}' ELSIF '(' condition ')' '{' statements '}' ELSE '{' BREAK '}'
    '''
    t[0] = node('[IF]')
    t[0].add(node(t[1]))
    t[0].add(node(t[2]))
    t[0].add(t[3])
    t[0].add(node(t[4]))
    t[0].add(node(t[5]))
    t[0].add(t[6])
    t[0].add(node(t[7]))
    if len(t)==19:
        t[0].add(node(t[8]))
        t[0].add(node(t[9]))
        t[0].add(t[10])
        t[0].add(node(t[11]))
        t[0].add(node(t[12]))
        t[0].add(t[13])
        t[0].add(node(t[14]))
        t[0].add(node(t[15]))
        t[0].add(node(t[16]))
        t[0].add(node(t[17]))
        t[0].add(node(t[18]))


def p_condition(t):
    '''condition : VARIABLE '>' VARIABLE
                 | VARIABLE '<' VARIABLE
                 | VARIABLE LESS VARIABLE
                 | VARIABLE '[' VARIABLE ']' '>' VARIABLE
                 | VARIABLE '[' VARIABLE ']' '<' VARIABLE
    '''
    if len(t) == 4:
        t[0] = simple_node(t, '[CONDITION]')
    elif len(t) == 7:
        t[0] = simple_node(t, '[CONDITION]')


def p_while(t):
    r'''while : WHILE '(' condition ')' '{' statements '}' '''
    if len(t) == 8:
        t[0] = node('[WHILE]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])
        t[0].add(node(t[4]))
        t[0].add(node(t[5]))
        t[0].add(t[6])
        t[0].add(node(t[7]))


def p_for(p):
    '''for : FOR '(' assignment ';' condition ';' operation ')' '{' statements '}' '''
    if len(p) == 12:
        p[0] = node('[FOR]')
        p[0].add(node(p[1]))
        p[0].add(node(p[2]))
        p[0].add(p[3])
        p[0].add(node(p[4]))
        p[0].add(p[5])
        p[0].add(node(p[6]))
        p[0].add(p[7])
        p[0].add(node(p[8]))
        p[0].add(node(p[9]))
        p[0].add(p[10])
        p[0].add(node(p[11]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)


yacc.yacc()
