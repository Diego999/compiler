import ply.lex as lex

reserved_words=(
    'afficher',
    'si',
    'sinon',
    'tantque',
    'pour',
)

tokens = (
    "NUMBER",
    "STRING",
    "BOOL",
    "PLUS_OP",
    "MINUS_OP",
    "TIME_OP",
    "DIVIDE_OP",
    "SMALLER_THAN",
    "SMALLER_EQUAL_THAN",
    "GREATER_THAN",
    "GREATER_EQUAL_THAN",
    "EQUAL",
    "ASSIGN",
    "TYPE",
    "IDENTIFIER",
)+ tuple(map(lambda s:s.upper(),reserved_words))

literals = '();{}'

def t_NUMBER(t):
    r'\d+(,\d*)*'
    return t

def t_STRING(t):
    r'".*"'
    
    return t

def t_BOOL(t):
    r'(vrai)|(faux)'
    return t

def t_PLUS_OP(t):
    r'plus'
    return t

def t_MINUS_OP(t):
    r'moins'
    return t

def t_TIME_OP(t):
    r'fois'
    return t

def t_DIVIDE_OP(t):
    r'divise par'
    return t

def t_SMALLER_THAN(t):
    r'plus petit que'
    return t

def t_SMALLER_EQUAL_THAN(t):
    r'plus petit ou egal que'
    return t

def t_GREATER_THAN(t):
    r'plus grand que'
    return t

def t_GREATER_EQUAL_THAN(t):
    r'plus grand ou egal que'
    return t

def t_EQUAL(t):
    r'est egal a'
    return t

def t_ASSIGN(t):
    r'egal'
    return t

def t_TYPE(t):
    r'(entier)|(reel)|(texte)|(booleen)'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z]+'
    if t.value in reserved_words:
       t.type = t.value.upper()
    return t
       
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
    import sys
    import os
    test_dir = "./tests/lex/"

    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        lex.input(prog)
        print(file)
        print("----------------------")
        while 1:
            tok = lex.token()
            if not tok:break
            print("line %d: %s(%s)" % (tok.lineno,tok.type,tok.value))
        print()
    
