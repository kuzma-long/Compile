#! /usr/bin/env python
#coding=utf-8
import ply.lex as lex
import ply.yacc as yacc
from node import node

def clear_text(text):
    lines=[]
    for line in text.split('\n'):
        line=line.strip()
        if len(line)>0:
            lines.append(line)
    return ' '.join(lines)


# TOKENS
tokens=('TITLE','ABS','DOC','SECTION','TEXT','BEGIN','END','LB','RB','AUTHOR','SUBSECTION','ITEMIZE','ITEM')

#DEFINE OF TOKENS
def t_TITLE(t):
    r'\\title'
    return t

def t_DOC(t):
    r'document'
    return t

def t_ABS(t):
    r'abstract'
    return t

def t_SECTION(t):
    r'\\section'
    return t


def t_BEGIN(t):
    r'\\begin'
    return t


def t_END(t):
    r'\\end'
    return t


def t_LB(t):
    r'\{'
    return t

def t_RB(t):
    r'\}'
    return t


def t_AUTHOR(t):
    r'\\author'
    return t


def t_SUBSECTION(t):
    r'\\subsection'
    return t


def t_ITEMIZE(t):
    r'itemize'
    return t


def t_ITEM(t):
    r'\\item'
    return t


def t_TEXT(t):
    r'[a-zA-Z\s\.\,\:\']+'
    return t


# IGNORED
t_ignore = " \t"
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# LEX
lex.lex()

# PARSE
def p_doc(p):
    r'doc : BEGIN LB DOC RB content END LB DOC RB'
    if len(p)==10:
        p[0]=node('[DOC]')
        p[0].add(p[5])

def p_content(p):
    r'content : title author abs sections TEXT'
    p[0]=node('[CONTENT]')
    p[0].add(p[1])
    p[0].add(p[2])
    p[0].add(p[3])
    p[0].add(p[4])
    p[0].add(node(p[5]))

def p_title(p):
    r'title : TITLE LB TEXT RB'
    if len(p)==5:
        p[0]=node('[TITLE]')
        p[0].add(node(p[3]))


def p_author(p):
    r'author : AUTHOR LB TEXT RB'
    p[0]=node('[AUTHOR]')
    p[0].add(node(p[3]))


def p_abs(t):
    r'abs : BEGIN LB ABS RB TEXT END LB ABS RB'
    if len(t)==10:
        t[0]=node('[ABSTRACT]')
        t[0].add(node(t[5]))


def p_sections(t):
    '''sections : sections section
                | section'''
    if len(t)==3:
        t[0]=node('[SECTIONS]')
        t[0].add(t[1])
        t[0].add(t[2])
    if len(t)==2:
        t[0]=node('[SECTIONS]')
        t[0].add(t[1])


def p_section(p):
    '''section : SECTION LB TEXT RB TEXT subsections
               | SECTION LB TEXT RB TEXT
    '''
    p[0] = node('[SECTION](%s)' % p[3])
    p[0].add(node(p[5]))
    if len(p)==7:
        p[0].add(p[6])


def p_subsections(p):
    '''subsections : subsections subsection
                   | subsection
    '''
    p[0] = node('[SUBSECTIONS]')
    p[0].add(p[1])
    if len(p) == 3:
        p[0].add(p[2])


def p_subsection(p):
    '''subsection : SUBSECTION LB TEXT RB TEXT itemize
                  | SUBSECTION LB TEXT RB TEXT
    '''
    p[0]=node('[SUBSECTION](%s)' % p[3])
    p[0].add(node(p[5]))
    if len(p)==7:
        p[0].add(p[6])


def p_itemize(p):
    '''itemize : BEGIN LB ITEMIZE RB items END LB ITEMIZE RB
    '''
    p[0] = node('[ITEMIZE]')
    p[0].add(p[5])


def p_items(p):
    '''items : items item
             | item
    '''
    p[0]=node('[ITEMS]')
    if len(p)==2:
        p[0].add(p[1])
    if len(p)==3:
        p[0].add(p[1])
        p[0].add(p[2])


def p_item(p):
    '''item : ITEM TEXT
    '''
    p[0]=node('[ITEM]')
    p[0].add(node(p[2]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)

data=clear_text(open('example2.tex','r').read())

yacc.yacc()

parse=yacc.parse(data)
parse.print_node(0)