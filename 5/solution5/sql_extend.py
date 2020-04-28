#! /usr/bin/env python
# coding=utf-8
import ply.lex as lex
import ply.yacc as yacc
import re
from math import *
from node import node

# TOKENS
tokens=('SELECT','FROM','WHERE','ORDER','BY','NAME','AND','OR','COMMA',
'LP','RP','AVG','BETWEEN','IN','SUM','MAX','MIN','COUNT','NUMBER','AS','DOT')

# Literals.  Should be placed in module given to lex()
literals = ['=','+','-','*', '^','>','<' ]


# DEFINE OF TOKENS
def t_SELECT(t):
    r'SELECT'
    return t


def t_FROM(t):
    r'FROM'
    return t


def t_WHERE(t):
    r'WHERE'
    return t


def t_ORDER(t):
    r'ORDER'
    return t


def t_BY(t):
    r'BY'
    return t


def t_AND(t):
    r'AND'
    return t


def t_OR(t):
    r'OR'
    return t


def t_COMMA(t):
    r','
    return t


def t_LP(t):
    r'\('
    return t


def t_RP(t):
    r'\)'
    return t


def t_AVG(t):
    r'AVG'
    return t


def t_BETWEEN(t):
    r'BETWEEN'
    return t


def t_IN(t):
    r'IN'
    return t


def t_SUM(t):
    r'SUM'
    return t


def t_MAX(t):
    r'MAX'
    return t


def t_MIN(t):
    r'MIN'
    return t


def t_COUNT(t):
    r'COUNT'
    return t


def t_NUMBER(t):
    r'\d+'
    return t


def t_AS(t):
    r'AS'
    return t


def t_DOT(t):
    r'\.'
    return t


def t_NAME(t):
    r'[A-Za-z]+|[a-zA-Z_][a-zA-Z0-9_]*|[A-Z]*\.[A-Z]$'
    return t


# IGNORED
t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# LEX ANALYSIS
lex.lex()


# PARSING
def p_query(p):
    '''query :  select
       | LP query RP
    '''
    if len(p)==2:
        p[0] = p[1]
    elif len(p)==4:
        p[0]=node('QUERY')
        p[0].add(node('('))
        p[0].add(p[2])
        p[0].add(node(')'))


def p_select(p):
    '''select :  SELECT list FROM table WHERE lst ORDER BY list
               | SELECT list FROM table WHERE lst
               | SELECT list FROM table ORDER BY list
               | SELECT list FROM table'''
    p[0] = node('QUERY')
    p[0].add(node('[SELECT]'))
    p[0].add(p[2])
    p[0].add(node('[FROM]'))
    p[0].add(p[4])
    if len(p)==7:
        p[0].add(node('[WHERE]'))
        p[0].add(p[6])
    elif len(p)==8:
        p[0].add(node('[ORDER]'))
        p[0].add(node('[BY]'))
        p[0].add(p[7])
    elif len(p)==10:
        p[0].add(node('[WHERE]'))
        p[0].add(p[6])
        p[0].add(node('[ORDER]'))
        p[0].add(node('[BY]'))
        p[0].add(p[9])


def p_table_1(p):
    '''table :  NAME'''
    p[0] = node('[TABLE]')
    p[0].add(node(p[1]))


def p_table_2(p):
    '''table : LP query RP'''
    p[0]=node('[TABLE]')
    p[0].add(node('('))
    p[0].add(p[2])
    p[0].add(node(')'))


def p_table_3(p):
    '''table : NAME AS NAME'''
    p[0]=node('[TABLE]')
    p[0].add(node(p[1]))
    p[0].add(node('[AS]'))
    p[0].add(node(p[3]))


def p_table_4(p):
    '''table : table AS NAME'''
    p[0]=node('[TABLE]')
    p[0].add(p[1])
    p[0].add(node('[AS]'))
    p[0].add(node(p[3]))


def p_table_5(p):
    '''table : table COMMA table'''
    p[0]=node('[TABLE]')
    p[0].add(p[1])
    p[0].add(node(','))
    p[0].add(p[3])


def p_lst(p):
    '''lst : condition
       | condition AND condition
       | condition OR condition
       | NAME BETWEEN NUMBER AND NUMBER
       | NAME IN LP query RP
    '''
    p[0]=node('[LST]')
    if len(p)==2:
        p[0].add(p[1])
    if len(p)==4:
        if p[2]=='AND':
            p[0].add(p[1])
            p[0].add(node('[AND]'))
            p[0].add(p[3])
        if p[2]=='OR':
            p[0].add(p[1])
            p[0].add(node('[OR]'))
            p[0].add(p[3])
    if len(p)==6:
        if p[4]=='AND':
            p[0].add(node(p[1]))
            p[0].add(node('[BETWEEN]'))
            p[0].add(node(p[3]))
            p[0].add(node('[AND]'))
            p[0].add(node(p[5]))
        else:
            p[0].add(node(p[1]))
            p[0].add(node('[IN]'))
            p[0].add(node('('))
            p[0].add(p[4])
            p[0].add(node(')'))


def p_condition(p):
    '''condition : NAME '<' agg
           | NAME '>' agg
           | NAME '=' agg
           | agg '>' NUMBER
           | agg '=' NUMBER
           | agg '<' NUMBER
           | NAME '<' NUMBER
           | NAME '>' NUMBER
           | NAME '=' NUMBER
           | NAME '<' NAME
           | NAME '=' NAME
           | NAME '>' NAME
           | NUMBER '<' NUMBER
           | NUMBER '>' NUMBER
           | NUMBER '=' NUMBER
           | agg '<' agg
           | agg '>' agg
           | agg '=' agg
    '''
    p[0] = node('[CONDITION]')
    p[0].add(node(p[1]))
    if p[2] == '<':
        p[0].add(node('<'))
    elif p[2] == '>':
        p[0].add(node('>'))
    elif p[2] == '=':
        p[0].add(node('='))
    p[0].add(p[3])


def p_agg_(p):
    '''agg :      SUM LP NAME RP
         | AVG LP NAME RP
         | COUNT LP NAME RP
         | MIN LP NAME RP
         | MAX LP NAME RP
         | COUNT LP '*' RP
'''
    p[0]=node('[AGG]')
    if p[1]=='SUM':
        p[0].add(node('[SUM]'))
    elif p[1]=='AVG':
        p[0].add(node('[AVG]'))
    elif p[1]=='COUNT':
        p[0].add(node('[COUNT]'))
    elif p[1]=='MIN':
        p[0].add(node('[MIN]'))
    elif p[1]=='MAX':
        p[0].add(node('[MAX]'))
    elif p[1]=='COUNT':
        p[0].add(node('[COUNT]'))
    p[0].add(node('('))
    p[0].add(node(p[3]))
    p[0].add(node(')'))


def p_list_1(p):
    ''' list : '*'
             | NAME'''
    p[0] = node('[FIELD]')
    p[0].add(node(p[1]))


def p_list_2(p):
    '''list : agg
    | NAME DOT NAME
    '''
    p[0]=node('[FIELD]')
    if len(p)==2:
        p[0].add(p[1])
    elif len(p)==4:
        p[0].add(node(p[1]))
        p[0].add(node('.'))
        p[0].add(node(p[3]))


yacc.yacc()

query = 'SELECT abc FROM def AS s WHERE df=SUM(nj) AND sd<AVG(ij) ORDER BY abc'

parse = yacc.parse(query)
parse.print_node(0)