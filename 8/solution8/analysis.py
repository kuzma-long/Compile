#! /usr/bin/env python
#coding=utf-8
from py_yacc import yacc
from util import clear_text
from translation import trans,v_table

text=clear_text(open('example.py','r').read())

# syntax parse
root=yacc.parse(text)
root.print_node(0)

# translation
trans(root)
print(v_table)