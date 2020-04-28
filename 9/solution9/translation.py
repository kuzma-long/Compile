#! /usr/bin/env python
# coding=utf-8
from __future__ import division

v_table = {}  # variable table


def update_v_table(name, value):
    v_table[name] = value


flag = 0


def trans(node):
    global flag
    # Translation

    # Assignment
    if node.getdata() == '[ASSIGNMENT]':
        '''assignment : VARIABLE '=' NUMBER
                      | VARIABLE '=' VARIABLE
                      | VARIABLE '=' '[' numbers ']'
                      | VARIABLE '=' VARIABLE '[' VARIABLE ']'
                      | VARIABLE '[' VARIABLE ']' '=' VARIABLE
                      | VARIABLE '[' VARIABLE ']' '=' VARIABLE '[' VARIABLE ']'
        '''
        if len(node.getchildren()) == 3:
            if node.getchild(2).getdata().isdigit():
                value = int(node.getchild(2).getdata())
            else:
                value =v_table[node.getchild(2).getdata()]
            node.getchild(0).setvalue(value)
            # update v_table
            update_v_table(node.getchild(0).getdata(), value)

        elif len(node.getchildren()) == 5:
            value = trans(node.getchild(3))
            node.getchild(0).setvalue(value)
            update_v_table(node.getchild(0).getdata(), value)
        elif len(node.getchildren()) == 6:
            if node.getchild(1).getdata() == '=':
                value = v_table[node.getchild(2).getdata()][v_table[node.getchild(4).getdata()]]
                node.getchild(0).setvalue(value)
                update_v_table(node.getchild(0).getdata(), value)
            elif node.getchild(1).getdata() == '[':
                value = v_table[node.getchild(5).getdata()]
                v_table[node.getchild(0).getdata()][v_table[node.getchild(2).getdata()]] = value
        elif len(node.getchildren()) == 9:
            value = v_table[node.getchild(5).getdata()][v_table[node.getchild(7).getdata()]]
            v_table[node.getchild(0).getdata()][v_table[node.getchild(2).getdata()]] = value

    # Numbers
    elif node.getdata()=='[NUMBERS]':
        '''numbers : numbers ',' NUMBER
                   | NUMBER
        '''
        if len(node.getchildren()) == 1:
            node.setvalue([node.getchild(0).getvalue()])
        else:
            node.setvalue(trans(node.getchild(0)) + [node.getchild(2).getvalue()])

    # Operation
    elif node.getdata() == '[OPERATION]':
        '''operation : VARIABLE '=' expression
                     | VARIABLE '=' LEN '(' VARIABLE ')'
                     | VARIABLE PLUS
        '''
        if len(node.getchildren()) == 2:
            value = v_table[node.getchild(0).getdata()] + 1
            v_table[node.getchild(0).getdata()] = value
            node.getchild(0).setvalue(value)
        elif len(node.getchildren()) == 3:
            value=trans(node.getchild(2))
            node.getchild(0).setvalue(value)
            update_v_table(node.getchild(0).getdata(), value)
        elif len(node.getchildren()) == 6:
            value = len(v_table[node.getchild(4).getdata()])
            node.getchild(0).setvalue(value)
            update_v_table(node.getchild(0).getdata(), value)

    # Expression
    elif node.getdata() == '[EXPRESSION]':
        '''expression : expression '+' term
                      | expression '-' term
                      | term
        '''
        if len(node.getchildren()) == 3:
            op = node.getchild(1).getdata()
            arg0 = trans(node.getchild(0))
            arg1 = trans(node.getchild(2))
            if op == '+':
                value = arg0 + arg1
            else:
                value = arg0 - arg1
            node.setvalue(value)
        else:
            node.setvalue(trans(node.getchild(0)))

    # TERM
    elif node.getdata() == '[TERM]':
        '''term : term '*' factor
                | term '/' factor
                | term DIVISION factor
                | factor
        '''
        if len(node.getchildren()) == 3:
            op = node.getchild(1).getdata()
            arg0 = trans(node.getchild(0))
            arg1 = trans(node.getchild(2))
            if op == '*':
                value = arg0 * arg1
            elif op=='//':
                value=arg0//arg1
            else:
                value = arg0 / arg1
            node.setvalue(value)
        else:
            node.setvalue(trans(node.getchild(0)))

    # FACTOR
    elif node.getdata() == '[FACTOR]':
        '''factor : VARIABLE
                  | '(' expression ')'
                  | NUMBER
        '''
        if len(node.getchildren()) == 1:
            if node.getchild(0).getdata().isdigit():
                node.setvalue(int(node.getchild(0).getdata()))
            else:
                node.setvalue(v_table[node.getchild(0).getdata()])
        else:
            node.setvalue(trans(node.getchild(1)))

    # Print
    elif node.getdata() == '[PRINT]':
        '''print : PRINT '(' VARIABLE ')' '''
        arg0 = v_table[node.getchild(2).getdata()]
        print(arg0)

    # If
    elif node.getdata() == '[IF]':
        r'''if : IF '(' condition ')' '{' statements '}'
               | IF '(' condition ')' '{' statements '}' ELSIF '(' condition ')' '{' statements '}' ELSE '{' BREAK '}'
         '''
        children = node.getchildren()
        if len(children)==7:
            if trans(children[2]):
                trans(children[5])
        else:
            if trans(children[2]):
                trans(children[5])
            elif trans(children[9]):
                trans(children[12])
            else:
                flag=1

    # While
    elif node.getdata() == '[WHILE]':
        r'''while : WHILE '(' condition ')' '{' statements '}' '''
        children = node.getchildren()
        while trans(children[2]):
            trans(children[5])
            if flag==1:
                break


    # For
    elif node.getdata()=='[FOR]':
        '''for : FOR '(' assignment ';' condition ';' operation ')' '{' statements '}' '''
        children=node.getchildren()
        trans(children[2])
        while trans(children[4]):
            trans(children[9])
            trans(children[6])

    # Condition
    elif node.getdata() == '[CONDITION]':
        '''condition : VARIABLE '>' VARIABLE
                     | VARIABLE '<' VARIABLE
                     | VARIABLE LESS VARIABLE
                     | VARIABLE '[' VARIABLE ']' '>' VARIABLE
                     | VARIABLE '[' VARIABLE ']' '<' VARIABLE
        '''
        if len(node.getchildren())==3:
            arg0 = v_table[node.getchild(0).getdata()]
            arg1 = v_table[node.getchild(2).getdata()]
            op = node.getchild(1).getdata()
            if op == '>':
                node.setvalue(arg0 > arg1)
            elif op == '<':
                node.setvalue(arg0 < arg1)
            elif op=='<=':
                node.setvalue(arg0<arg1 or arg0==arg1)
        elif len(node.getchildren())==6:
            arg0=v_table[node.getchild(0).getdata()][v_table[node.getchild(2).getdata()]]
            arg1=v_table[node.getchild(5).getdata()]
            op=node.getchild(4).getdata()
            if op=='>':
                node.setvalue(arg0 > arg1)
            elif op == '<':
                node.setvalue(arg0 < arg1)

    else:
        for c in node.getchildren():
            trans(c)

    return node.getvalue()
