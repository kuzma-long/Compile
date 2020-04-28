import ply.lex as lex

# List of token names.   This is always required
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'LBRACE',
   'RBRACE',
   'ID',
   'EQUAL',
   'OUT',
   'LESSTHAN',
   'SEMICOLON',
   'QUOTES',
   'DOT'
]

# Regular expression rules for simple tokens
t_OUT     = r'<<'
t_PLUS    = r'\+'
t_EQUAL   = r'='
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LESSTHAN= r'<'
t_SEMICOLON=r';'
t_QUOTES  = r'"'
t_DOT     = r'\.'


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# 处理保留字
reserved = {
    'if' : 'IF',
    'int': 'INT',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
     }
tokens = tokens + list(reserved.values())


def t_ID(t):
   r'[a-zA-Z_][a-zA-Z_0-9]*'
   t.type = reserved.get(t.value,'ID')    # Check for reserved words
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

# Test it out
data = '''
int asd = 0;
int bc = 10;
while ( asd < bc)
{
	if(bc - asd < 2)
		cout<<"they are close."<<endl;
	asd = asd + 1;
}
'''
# Give the lexer some input
lexer.input(data)
# Tokenize
while True:
    tok = lexer.token()
    if not tok: break # No more input
    print(tok)