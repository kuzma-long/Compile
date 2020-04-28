import ply.yacc as yacc
import ply.lex as lex


#存储分子式的数据结构
class Atom(object):
    def __init__(self, symbol, count):
        self.symbol = symbol
        self.count = count

    def __repr__(self):
        return "Atom(%r, %r)" % (self.symbol, self.count)


# List of token names.   This is always required
tokens = [
    'SYMBOL',
    'COUNT'
]

# A regular expression rule for symbol
t_SYMBOL = (
    r"C[laroudsemf]?|Os?|N[eaibdpos]?|S[icernbmg]?|P[drmtboau]?|"
    r"H[eofgas]?|A[lrsgutcm]|B[eraik]?|Dy|E[urs]|F[erm]?|G[aed]|"
    r"I[nr]?|Kr?|L[iaur]|M[gnodt]|R[buhenaf]|T[icebmalh]|"
    r"U|V|W|Xe|Yb?|Z[nr]")


# A regular expression rule for count with some action code
def t_COUNT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


def p_species_list_species(p):
    'species_list :  species_list species'
    p[0] = p[1] + p[2]


def p_species_list(p):
    'species_list :  species'
    p[0] = p[1]


def p_species_symbol(p):
    'species :     SYMBOL'
    p[0] = 1


def p_species_symbol_count(p):
    'species :     SYMBOL COUNT'
    p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()


while True:
    try:
        s = input('formula > ')
    except EOFError:                                     #处理以Ctrl-d结尾的异常
        break
    if not s:
        continue
    if s=='finish':                                      #当输入finish时，结束当前程序
        break
    result=parser.parse(s)
    print(result)