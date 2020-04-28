#! /usr/bin/env python
#coding=utf-8
import ply.lex as lex

# LEX for parsing Python

# Tokens
tokens=('VARIABLE','NUMBER','DEF','RETURN','CLASS')

literals=['=','+','-','*','(',')','{','}','<','>','.',"'",',']

#Define of tokens

def t_NUMBER(t):
    r'[0-9]+'
    return t

def t_DEF(t):
    r'def'
    return t

def t_RETURN(t):
    r'return'
    return t


def t_CLASS(t):
    r'class'
    return t


def t_VARIABLE(t):
    r'[a-zA-Z_]+'
    return t


# Ignored
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lex.lex()
