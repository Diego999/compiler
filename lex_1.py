import ply.lex as lex

reserved_words_upper=(
    'si',
    'sinon',
    'pour'
)

reserved_words_lower=(
    'afficher',
    'de',
    'a'
)

tokens = (
    "NUMBER",
    "STRING",
    "BOOL",
    "SMALLER_THAN",
    "SMALLER_EQUAL_THAN",
    "GREATER_THAN",
    "GREATER_EQUAL_THAN",
    "PLUS_OP",
    "MINUS_OP",
    "TIME_OP",
    "DIVIDE_OP",
    "EQUAL",
    "ASSIGN",
    "TYPE",
    "IDENTIFIER",
    "BY_STEP",
    "WHILE"

)+ tuple(map(lambda s: s.upper(), reserved_words_upper)) + tuple(map(lambda s: s.lower(), reserved_words_lower))

literals = '();{}'

error_output = open('outputs/' + 'error_lex.log', 'w')
error_number = 0

def t_NUMBER(t):
    r'\d+(,\d*)*'
    return t


def t_STRING(t):
    r'".*"'
    return t


def t_BOOL(t):
    r'(vrai)|(faux)'
    return t


def t_SMALLER_THAN(t):
    r'plus\spetit\sque'
    return t


def t_SMALLER_EQUAL_THAN(t):
    r'plus\spetit\sou\segal\sque'
    return t


def t_GREATER_THAN(t):
    r'plus\sgrand\sque'
    return t


def t_GREATER_EQUAL_THAN(t):
    r'plus\sgrand\sou\segal\sque'
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
    r'divise\spar'
    return t


def t_EQUAL(t):
    r'est\segal\sa'
    return t


def t_ASSIGN(t):
    r'egal'
    return t


def t_TYPE(t):
    r'(entier)|(reel)|(texte)|(booleen)'
    return t


def t_BY_STEP(t):
    r'par\spas\sde'
    return t


def t_WHILE(t):
    r'TANT\sQUE'
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z]+'
    if t.value.lower() in reserved_words_upper:
       t.type = t.value.upper()
    if t.value.lower() in reserved_words_lower:
        t.type = t.value.lower()
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '


def t_error(t):
    error_output.write("Illegal character '%s'\n" % t.value[0])
    global error_number
    error_number += 1
    t.lexer.skip(1)


def generate_lex(prog, title):
    error_output.write('=============='+title+'==============\n')
    global error_number
    error_number = 0
    lex.lex()
    lex.input(prog)
    while 1:
            if not lex.token():
                break
    lex.lex()
    error_output.write('\n')
    error_output.write(error_number.__str__())
    error_output.write(" errors !!\n")
    return error_number

lex.lex()

if __name__ == "__main__":
    import os

    test_dir = "./tests/"
    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        generate_lex(prog, file.split(".")[0])
