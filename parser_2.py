import ply.yacc as yacc
import AST
from lex_1 import tokens, generate_lex

default_values = {
    'entier': '0',
    'reel': '0,0',
    'texte': '""',
    'booleen': 'faux',
}

precedence = (
    ('left', 'PLUS_OP'),
    ('left', 'MINUS_OP'),
    ('left', 'TIME_OP'),
    ('left', 'DIVIDE_OP'),
    ('right', 'UMINUS'),
)

error_parser = open('outputs/' + 'error_parser.log', 'w')
error_number = 0

def p_programme_statement(p):
    """programme : statement"""
    p[0] = AST.ProgramNode(p[1])


def p_programme_recursive(p):
    """programme : statement programme"""
    p[0] = AST.ProgramNode([p[1]]+p[2].children)


def p_statement(p):
    """statement : assignation ';'
                | structure ';'"""
    p[0] = p[1]


def p_statement_afficher(p):
    """statement : afficher expression ';'"""
    p[0] = AST.PrintNode(p[2])


def p_if(p):
    """structure : SI '(' expression ')' '{' programme '}'"""
    p[0] = AST.IfNode([p[3], p[6]])


def p_if_else(p):
    """structure : SI '(' expression ')' '{' programme '}' SINON '{' programme '}'"""
    p[0] = AST.IfNode([p[3], p[6], p[10]])


def p_declaration(p):
    """assignation : IDENTIFIER TYPE"""
    p[0] = AST.AssignNode([AST.TokenNode(p[1])] + [AST.TokenNode(p[2]), AST.TokenNode(default_values[p[2]])])


def p_declaration_assignation(p):
    """assignation : IDENTIFIER TYPE ASSIGN expression"""
    p[0] = AST.AssignNode([AST.TokenNode(p[1])] + [AST.TokenNode(p[2]), p[4]])


def p_assignation(p):
    """assignation : IDENTIFIER ASSIGN expression"""
    p[0] = AST.AssignNode([AST.TokenNode(p[1])] + [p[3]])


def p_expression_op(p):
    """expression : expression PLUS_OP expression
                | expression MINUS_OP expression
                | expression TIME_OP expression
                | expression DIVIDE_OP expression"""
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_bool(p):
    """expression : expression SMALLER_THAN expression
            | expression SMALLER_EQUAL_THAN expression
            | expression GREATER_THAN expression
            | expression GREATER_EQUAL_THAN expression
            | expression EQUAL expression"""
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_num(p):
    """expression : NUMBER
                | BOOL
                | STRING
                | IDENTIFIER"""
    p[0] = AST.TokenNode(p[1])


def p_expression_paren(p):
    """expression : '(' expression ')' """
    p[0] = p[2]


def p_for(p):
    """structure : POUR '(' IDENTIFIER de NUMBER a NUMBER BY_STEP expression ')' '{' programme '}'
                | POUR '(' IDENTIFIER de NUMBER a IDENTIFIER BY_STEP expression ')' '{' programme '}'"""
    p[0] = AST.ForNode([
        AST.AssignNode([AST.TokenNode(p[3])] + [AST.TokenNode('entier'), AST.TokenNode(p[5])]),  # Initialization
        AST.IfNode([AST.OpNode('plus petit ou egal que', [AST.TokenNode(p[3]), AST.TokenNode(p[7])]), p[12]]),  # Condition
        AST.AssignNode([AST.TokenNode(p[3])] + [AST.OpNode('plus', [AST.TokenNode(p[3]), p[9]])])  # Inc
    ])

def p_while(p):
    """structure : WHILE '(' expression ')' '{' programme '}' """
    p[0] = AST.WhileNode([p[3]] + [p[6]])


def p_minus(p):
    """expression : PLUS_OP expression %prec UMINUS
                | MINUS_OP expression %prec UMINUS"""
    p[0] = AST.OpNode(p[1], [p[2]])


def p_error(p):
    global error_number
    error_number += 1
    if p:
        error_parser.write("Syntax error in line %d, position %d \n" % (p.lineno, p.lexpos))
        yacc.errok()
    else:
        error_parser.write("Sytax error: unexpected end of file\n")

yacc.yacc(outputdir='generated')


def generate_parser(program, title):
    error_parser.write('=============='+title+'==============\n')
    global error_number
    error_number = 0
    yacc.lineno = yacc.lexpos = 0


    out = yacc.parse(program, tracking=True)
    error_parser.write('\n')
    error_parser.write(error_number.__str__())
    error_parser.write(" errors !!\n")
    if out:
        graph = out.makegraphicaltree()
        graph.write_pdf('pdf/' + title.split(".")[0] + '−ast.pdf')
    return error_number, out


if __name__ == "__main__":
    import os
    test_dir = "./tests/"

    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        try:
            name = file.split('.')[0]
            (err_num, result) = generate_parser(prog, file)
            if result:
                graph = result.makegraphicaltree()
                graph.write_pdf('pdf/' + name + '−ast.pdf')
        except Exception as e:
            print(e)
