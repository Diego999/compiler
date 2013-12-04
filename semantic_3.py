import AST
import re
import sys
from AST import addToClass
from parser_2 import parse

var_type = {}

TYPE_TEXT = 'texte'
TYPE_INT = 'entier'
TYPE_DOUBLE = 'reel'
TYPE_BOOL = 'booleen'
BOOL_TRUE = 'vrai'
BOOL_FALSE = 'faux'
TYPE_VAR = "variable"
TYPE_INVALID = "invalide"

@addToClass(AST.TokenNode)
def execute(self):
    if self.tok[0] == '"' and self.tok[-1] == '"':
        return TYPE_TEXT
    elif self.tok == BOOL_TRUE or self.tok == BOOL_FALSE:
        return TYPE_BOOL
    elif self.tok.find(',') != -1:
        try:
            self.tok = self.tok.replace(',','.')
            float(self.tok)
            return TYPE_DOUBLE
        except:
            return TYPE_INVALID
    else:
        try:
            int(self.tok)
            return TYPE_INT
        except:
            regex = re.compile(r'[a-zA-Z]+')
            if regex.match(self.tok) != None:
                return TYPE_VAR
            else:
                return TYPE_INVALID
    
@addToClass(AST.OpNode)
def execute(self):
    type1 = self.children[0].execute()
    type2 = self.children[1].execute()
    if type1 != TYPE_DOUBLE and type1 != TYPE_INT or type2 != TYPE_DOUBLE and type2 != TYPE_INT:
          print("Incompatible types")
          sys.exit(-1)
    elif type1 == type2:
        return type1
    else:
        return TYPE_DOUBLE

@addToClass(AST.AssignNode)
def execute(self):
    print("Assign : ",self.children)
    left_exp_type = None
    right_exp_type = None
    if len(self.children) == 2:
        if self.children[0].execute()==TYPE_VAR:
            if var_type.__contains__(self.children[0].tok):
                left_exp_type = var_type[self.children[0].tok]
                right_exp_type = self.children[1].execute()
                
            else:
                print("Undefined variable")
                sys.exit(-1)
            
        else:
            print("Cannot assign value to a constant")
    elif len(self.children) == 3:
        if self.children[0].execute()==TYPE_VAR:
            if var_type.__contains__(self.children[0].tok):
                left_exp_type = var_type[self.children[0].tok]
                if left_exp_type != self.children[1].tok:
                    print("Type does not match")
                    sys.exit(-1)
                    return
            else:
                var_type[self.children[0].tok] = self.children[1].tok
                left_exp_type = self.children[1].tok
            right_exp_type = self.children[2].execute()
    if left_exp_type != right_exp_type:
        print("Type does not match")
        sys.exit(-1)
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
    try:
        prog = "aa reel egal 2,0 plus 2 moins 2;"
        execute(parse(prog))
    except:
        pass
    """for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        print(file)
        print("----------------------")
        result = parse(prog)
        execute(result)"""
