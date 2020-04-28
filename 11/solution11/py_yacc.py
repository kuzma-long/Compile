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
                  | function
                  | runfunction
                  | class
    '''
    if len(t)==2:
        t[0]=node(['STATEMENT'])
        t[0].add(t[1])
        
def p_assignment(t):
    '''assignment : VARIABLE '.' VARIABLE '=' VARIABLE
                  | VARIABLE '=' VARIABLE '(' string ',' numbers ')'
    '''
    if len(t)==6:
        t[0]=simple_node(t,'[ASSIGNMENT]')
    elif len(t)==9:
        t[0]=node('[ASSIGNMENT]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(node(t[4]))
        t[0].add(t[5])
        t[0].add(node(t[6]))
        t[0].add(t[7])
        t[0].add(node(t[8]))


def p_string(p):
    '''string : "'" VARIABLE "'" '''
    if len(p)==4:
        p[0]=simple_node(p,'[STRING]')


def p_numbers(p):
    '''numbers : numbers ',' NUMBER
               | NUMBER
    '''
    p[0]=node('[NUMBERS]')
    if len(p)==4:
        p[0].add(p[1])
        p[0].add(node(p[2]))
        p[0].add(node(p[3]))
    elif len(p)==2:
        p[0].add(node(p[1]))


def p_operation(t):
    '''operation : VARIABLE '.' VARIABLE '=' VARIABLE '.' VARIABLE '+' VARIABLE'''
    if len(t)==10:
        t[0]=simple_node(t,'[OPERATION]')


def p_function(t):
    r'''function : DEF VARIABLE '(' variables ')' '{' statements RETURN VARIABLE '}'
                 | DEF VARIABLE '(' variables ')' '{' statements '}'
    '''
    t[0] = node('[FUNCTION]')
    t[0].add(node(t[1]))
    t[0].add(node(t[2]))
    t[0].add(node(t[3]))
    t[0].add(t[4])
    t[0].add(node(t[5]))
    t[0].add(node(t[6]))
    t[0].add(t[7])
    t[0].add(node(t[8]))
    if len(t)==11:
        t[0].add(node(t[9]))
        t[0].add(node(t[10]))


def p_variables(p):
    '''variables : variables ',' VARIABLE
                 | VARIABLE
    '''
    p[0]=node('[VARIABLES]')
    if len(p)==4:
        p[0].add(p[1])
        p[0].add(node(p[2]))
        p[0].add(node(p[3]))
    elif len(p)==2:
        p[0].add(node(p[1]))


def p_runfunction(t):
    r'''runfunction : VARIABLE '(' variables ')'
                    | VARIABLE '.' VARIABLE '(' numbers ')'
                    | VARIABLE '.' VARIABLE '(' ')'
    '''
    if len(t)==5:
        t[0]=simple_node(t,'[REFUNCTION]')
    elif len(t)==7:
        t[0]=node('[REFUNCTION]')
        t[0].add(node(t[1]))
        t[0].add(node(t[2]))
        t[0].add(node(t[3]))
        t[0].add(node(t[4]))
        t[0].add(t[5])
        t[0].add(node(t[6]))
    elif len(t)==6:
        t[0] = simple_node(t, '[REFUNCTION]')
        
def p_class(p):
    '''class : CLASS VARIABLE '{' functions '}' '''
    if len(p)==6:
        p[0]=node('[CLASS]')
        p[0].add(node(p[1]))
        p[0].add(node(p[2]))
        p[0].add(node(p[3]))
        p[0].add(p[4])
        p[0].add(node(p[5]))


def p_functions(p):
    '''functions : functions function
                 | function
    '''
    p[0]=node('[FUNCTIONS]')
    if len(p)==3:
        p[0].add(p[1])
        p[0].add(p[2])
    elif len(p)==2:
        p[0].add(p[1])

                
def p_error(t):
    print("Syntax error at '%s'" % t.value)
    # print(t)

yacc.yacc()
