import AST
from AST import addToClass
from parser_2 import parse

var_type = {}

TYPE_TEXT = 'texte'
TYPE_INT = 'entier'
TYPE_DOUBLE = 'reel'
TYPE_BOOL = 'booleen'
BOOL_TRUE = 'vrai'
BOOL_FALSE = 'faux'

@addToClass(AST.TokenNode)
def execute(self):
    if self.tok == "aa":
        if self.tok[0] == '"' and self.tok[-1] == '"':
            return TYPE_TEXT
        elif self.tok == BOOL_TRUE or self.tok == BOOL_FALSE:
            return TYPE_BOOL
        elif self.tok.find(',') != -1:
            try:
                float(self.tok)
                return TYPE_DOUBLE
            except:
                pass
        else:
            try:
                int(self.tok)
                return TYPE_INT
            except:
                pass
            if var_type.__contains__(self.tok):
                return var_type[self.tok]
            else:
                print("Variable's name is undefined")

@addToClass(AST.OpNode)
def execute(self):
    return self

@addToClass(AST.AssignNode)
def execute(self):
    for c in self.children:
        c.execute()
    return self

@addToClass(AST.IfNode)
@addToClass(AST.ForNode)
@addToClass(AST.WhileNode)
@addToClass(AST.ProgramNode)
@addToClass(AST.PrintNode)
def execute(self):
    for c in self.children:
        c.execute()

if __name__ == "__main__":
    import os
    test_dir = "./tests/semantic/"

    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        print(file)
        print("----------------------")
        result = parse(prog)
        execute(result)