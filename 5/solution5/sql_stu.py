#! /usr/bin/env python
# coding=utf-8
import ply.lex as lex
import ply.yacc as yacc
import pandas
import re
from math import *
from node import node

pandas.set_option('display.max_rows', None)
student = pandas.read_csv("./student.csv",encoding='gbk')
student.rename(columns={'考号':'Sno','语文':'Chinese','数学':'Math', '英语':'English', '总分':'Sum'},inplace=True)

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


'''SELECT AVG(Math) FROM Student'''
def p_select1(p):
    '''select : SELECT list FROM table'''
    p[0] = node('QUERY')
    p[0].add(node('[SELECT]'))
    p[0].add(p[2])
    p[0].add(node('[FROM]'))
    p[0].add(p[4])
    if p[2].getchildren()[0].getdata()=='*':
        p[0].table=p[4].table
    elif p[2].getchildren()[0].getdata() == '[AGG]':
        if p[2].getchildren()[0].getchildren()[0].getdata() == '[MAX]':
            column = p[2].getchildren()[0].getchildren()[2].getdata() #需要查询的列
            table1 = p[4].table.loc[:,[column]]
            p[0].table = table1.max() #计算最大值
        if p[2].getchildren()[0].getchildren()[0].getdata() == '[AVG]':
            column = p[2].getchildren()[0].getchildren()[2].getdata() #需要查询的列
            table1 = p[4].table.loc[:,[column]]
            p[0].table = table1.mean()#计算平均值


'''SELECT Sno FROM Student WHERE Chinese IN (SELECT MAX(Chinese) FROM Student)'''
def p_select2(p):
    '''select : SELECT list FROM table WHERE lst'''
    p[0] = node('QUERY')
    p[0].add(node('[SELECT]'))
    p[0].add(p[2])
    p[0].add(node('[FROM]'))
    p[0].add(p[4])
    p[0].add(node('[WHERE]'))
    p[0].add(p[6])
    if (p[6].getchildren()[1].getdata() == '[IN]'):
        table1 = p[6].getchildren()[3].table#子查询列表
        column1 = p[2].getchildren()[0].getdata()#最终需要的列
        column2 = p[6].getchildren()[0].getdata()#Where字句里面的列
        table2 = p[4].table
        p[0].table = table2[table2[column2].isin(table1)].loc[:,[column1,column2]]


'''SELECT * FROM Student ORDER BY Sum'''
def p_select3(p):
    '''select : SELECT list FROM table ORDER BY list'''
    p[0] = node('QUERY')
    p[0].add(node('[SELECT]'))
    p[0].add(p[2])
    p[0].add(node('[FROM]'))
    p[0].add(p[4])
    p[0].add(node('[ORDER]'))
    p[0].add(node('[BY'))
    p[0].add(p[7])
    if p[2].getchildren()[0].getdata() == '*':
        column = p[7].getchildren()[0].getdata()#获取排序对应的列
        p[0].table = p[4].table.sort_values(by=column,ascending=False)#ascending=False倒序排序


def p_select4(p):
    ''' select :  SELECT list FROM table WHERE lst ORDER BY list'''
    p[0] = node('QUERY')
    p[0].add(node('[SELECT]'))
    p[0].add(p[2])
    p[0].add(node('[FROM]'))
    p[0].add(p[4])
    p[0].add(node('[WHERE]'))
    p[0].add(p[6])
    p[0].add(node('[ORDER]'))
    p[0].add(node('[BY]'))
    p[0].add(p[9])


def p_table_1(p):
    '''table :  NAME'''
    p[0] = node('[TABLE]')
    p[0].add(node(p[1]))
    p[0].table=student


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

print('第1次查询结果如下：')
query1 = 'SELECT Sno FROM Student WHERE Chinese IN (SELECT MAX(Chinese) FROM Student)'
parse = yacc.parse(query1)
parse.print_node(0)
print(parse.table)
print()

print('第2次查询结果如下：')
query2 = 'SELECT * FROM Student ORDER BY Sum'
parse = yacc.parse(query2)
parse.print_node(0)
print(parse.table)
print()

print('第3次查询结果如下：')
query3 = 'SELECT AVG(Math) FROM Student'
parse = yacc.parse(query3)
parse.print_node(0)
print(parse.table)
print()