import ply.yacc as yacc
import AST
from lex_1 import tokens

default_values = {
    'entier': '0',
    'reel': '0.0',
    'texte': '',
    'booleen': 'faux',
}

precedence = (
    ('left', 'PLUS_OP'),
    ('left', 'MINUS_OP'),
    ('left', 'TIME_OP'),
    ('left', 'DIVIDE_OP'),
    ('right', 'UMINUS'),
)


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
    """structure : POUR '(' IDENTIFIER de NUMBER a NUMBER BY_STEP expression ')' '{' programme '}'"""
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
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print("Sytax error: unexpected end of file!")

yacc.yacc(outputdir='generated')


def parse(program):
    return yacc.parse(program)#, debug=1)


if __name__ == "__main__":
    import os
    test_dir = "./tests/parser/"

    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        print(file)
        print("----------------------")
        try:
            
            result = parse(prog)
            print(result)
            graph = result.makegraphicaltree()
            name = 'pdf/' + file.split('.')[0] + '−ast.pdf'
            graph.write_pdf(name)
        except:
            print("\nCould not be generated");
