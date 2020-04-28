#! /usr/bin/env python
#coding=utf-8
from py_yacc import yacc
from util import clear_text

text=clear_text(open('stu.py','r').read())

# syntax parse
root=yacc.parse(text)
root.print_node(0)