#! /usr/bin/env python
# coding=utf-8
from __future__ import division

v_table = {}  # variable table


def update_v_table(name, value):
    v_table[name] = value


def trans(node):
    for c in node.getchildren():
        trans(c)

    # Translation

    # Assignment
    if node.getdata() == '[ASSIGNMENT]':
        ''' statement : VARIABLE '=' NUMBER'''
        value = node.getchild(2).getvalue()
        node.getchild(0).setvalue(value)
        # update v_table
        update_v_table(node.getchild(0).getdata(), value)

    # Operation
    elif node.getdata() == '[OPERATION]':
        '''operation : VARIABLE '=' expression'''
        value = node.getchild(2).getvalue()
        node.getchild(0).setvalue(value)
        # update v_table
        update_v_table(node.getchild(0).getdata(), value)

    # Expression
    elif node.getdata() == '[EXPRESSION]':
        '''expression : expression '+' term
                      | expression '-' term
                      | term
        '''
        if len(node.getchildren()) == 3:
            op = node.getchild(1).getdata()
            arg0 = node.getchild(0).getvalue()
            arg1 = node.getchild(2).getvalue()
            if op == '+':
                value = arg0 + arg1
            else:
                value = arg0 - arg1
            node.setvalue(value)
        else:
            node.setvalue(node.getchild(0).getvalue())

    # TERM
    elif node.getdata() == '[TERM]':
        '''term : term '*' factor
                | term '/' factor
                | factor
        '''
        if len(node.getchildren()) == 3:
            op = node.getchild(1).getdata()
            arg0 = node.getchild(0).getvalue()
            arg1 = node.getchild(2).getvalue()
            if op == '*':
                value = arg0 * arg1
            else:
                value = arg0 / arg1
            node.setvalue(value)
        else:
            node.setvalue(node.getchild(0).getvalue())

    # FACTOR
    elif node.getdata() == '[FACTOR]':
        '''factor : VARIABLE
                  | '(' expression ')'
                  | NUMBER
        '''
        if len(node.getchildren()) == 1:
            if node.getchild(0).getdata().isdigit():
                node.setvalue(node.getchild(0).getvalue())
            else:
                node.setvalue(v_table[node.getchild(0).getdata()])
        else:
            node.setvalue(node.getchild(1).getvalue())

    # VARIABLES
    elif node.getdata()=='[VARIABLES]':
        '''variables : variables ',' VARIABLE
                     | VARIABLE
        '''
        if len(node.getchildren())==1:
            node.setvalue([node.getchild(0).getdata()])
        else:
            node.setvalue(node.getchild(0).getvalue()+[node.getchild(2).getdata()])

    # Print
    elif node.getdata() == '[PRINT]':
        '''print : PRINT '(' variables ')' '''
        for i in node.getchild(2).getvalue():
            print(v_table[i],end='\t')
        print()
