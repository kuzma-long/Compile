#! /usr/bin/env python
#coding=utf-8
import ply.yacc as yacc
from py_lex import *
from node import node,num_node

# YACC for parsing Python

def simple_node(t,name):
    t[0]=node(name)
    for i in range(1,len(t)):
        t[0].add(node(t[i]))
    return t[0]

def p_program(t):
    '''program : statements'''
    if len(t)==2:
        t[0]=node('[PROGRAM]')
        t[0].add(t[1])
        
def p_statements(t):
    '''statements : statements statement
                  | statement'''
    if len(t)==3:
        t[0]=node('[STATEMENTS]')
        t[0].add(t[1])
        t[0].add(t[2])
    elif len(t)==2:
        t[0]=node('[STATEMENTS]')
        t[0].add(t[1])

def p_statement(t):
    ''' statement : assignment
                  | operation
                  | print
                  | if
                  | while
                  | function
                  | runfunction
                  | return
    '''
    if len(t)==2:
        t[0]=node(['STATEMENT'])
        t[0].add(t[1])
        
def p_assignment(t):
    '''assignment : VARIABLE '=' VARIABLE
                  | VARIABLE '=' '[' numbers ']'
                  | VARIABLE '=' VARIABLE '[' VARIABLE ']'
                  | VARIABLE '[' VARIABLE ']' '=' VARIABLE
                  | VARIABLE '[' VARIABLE ']' '=' VARIABLE '[' VARIABLE ']'
    '''
    if len(t)==6:
        t[0]=node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(t[4])
        t[0].add(node(t[5]))
    else:
        t[0]=simple_node(t,'[ASSIGNMENT]')


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


def p_operation(t):
    '''operation : VARIABLE PLUSEQUAL NUMBER
                 | VARIABLE MINEQUAL NUMBER
    '''
    if len(t)==4:
        t[0]=simple_node(t,'[OPERATION]')


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
              | LEN '(' VARIABLE ')'
    '''
    if len(p) == 2:
        p[0] = node('[FACTOR]')
        if p[1].isdigit():
            p[0].add(num_node(p[1]))
        else:
            p[0].add(node(p[1]))
    elif len(p) == 4:
        p[0] = node('[FACTOR]')
        p[0].add(node('('))
        p[0].add(p[2])
        p[0].add(node(')'))
    elif len(p)==5:
        p[0]=simple_node(p,'[FACTOR]')


def p_print(t):
    '''print : PRINT '(' VARIABLE ')' '''
    if len(t)==5:
        t[0]=simple_node(t,'[PRINT]')
                
def p_if(t):
    r'''if : IF '(' condition ')' '{' statements '}' '''
    if len(t)==8:
        t[0]=node('[IF]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])
        t[0].add(node(t[4]))
        t[0].add(node(t[5]))
        t[0].add(t[6])
        t[0].add(node(t[7]))

def p_function(t):
    r'''function : DEF VARIABLE '(' VARIABLE ',' VARIABLE ',' VARIABLE ')' '{' statements '}' '''
    if len(t)==13:
        t[0]=node('[FUNCTION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(node(t[4]))
        t[0].add(node(t[5]))
        t[0].add(node(t[6]))
        t[0].add(node(t[7]))
        t[0].add(node(t[8]))
        t[0].add(node(t[9]))
        t[0].add(node(t[10]))
        t[0].add(t[11])
        t[0].add(node(t[12]))

def p_runfunction1(t):
    r'''runfunction : VARIABLE '(' VARIABLE ',' VARIABLE ',' expression ')' '''
    if len(t)==9:
        t[0]=node('[RUNFUNCTION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(node(t[4]))
        t[0].add(node(t[5]))
        t[0].add(node(t[6]))
        t[0].add(t[7])
        t[0].add(node(t[8]))


def p_runfunction2(t):
    r'''runfunction : VARIABLE '(' VARIABLE ',' expression ',' VARIABLE ')' '''
    if len(t)==9:
        t[0]=node('[RUNFUNCTION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(node(t[4]))
        t[0].add(t[5])
        t[0].add(node(t[6]))
        t[0].add(node(t[7]))
        t[0].add(node(t[8]))


def p_runfunction3(t):
    r'''runfunction : VARIABLE '(' VARIABLE ',' NUMBER ',' expression ')' '''
    if len(t)==9:
        t[0]=node('[RUNFUNCTION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(node(t[4]))
        t[0].add(num_node(t[5]))
        t[0].add(node(t[6]))
        t[0].add(t[7])
        t[0].add(node(t[8]))


def p_return(p):
    '''return : RETURN'''
    if len(p)==2:
        p[0]=simple_node(p,'[RETURN]')


def p_condition(t):
    '''condition : VARIABLE MORE VARIABLE
                 | VARIABLE '<' VARIABLE
                 | VARIABLE '[' VARIABLE ']' '>' VARIABLE
                 | VARIABLE '[' VARIABLE ']' LESS VARIABLE
    '''
    t[0]=simple_node(t,'[CONDITION]')

def p_while(t):
    r'''while : WHILE '(' condition ')' '{' statements '}'
              | WHILE '(' condition AND condition ')' '{' statements '}'
    '''
    if len(t)==8:
        t[0]=node('[WHILE]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])
        t[0].add(node(t[4]))
        t[0].add(node(t[5]))
        t[0].add(t[6])
        t[0].add(node(t[7]))
    elif len(t)==10:
        t[0] = node('[WHILE]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(t[3])
        t[0].add(node(t[4]))
        t[0].add(t[5])
        t[0].add(node(t[6]))
        t[0].add(node(t[7]))
        t[0].add(t[8])
        t[0].add(node(t[9]))
    
                
def p_error(t):
    print("Syntax error at '%s'" % t.value)

yacc.yacc()
