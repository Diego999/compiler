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

OPERATION_TYPE = {
    'plus' : [TYPE_TEXT,TYPE_INT,TYPE_DOUBLE],
    'moins' : [TYPE_INT,TYPE_DOUBLE],
    'divise par' : [TYPE_INT,TYPE_DOUBLE],
    'fois' : [TYPE_INT,TYPE_DOUBLE],
    'plus petit que' : [TYPE_INT,TYPE_DOUBLE],
    'plus grand que' : [TYPE_INT,TYPE_DOUBLE],
    'plus petit ou egal que' : [TYPE_INT,TYPE_DOUBLE],
    'plus grand ou egal que' : [TYPE_INT,TYPE_DOUBLE],
    'est egal a' : [TYPE_INT,TYPE_DOUBLE,TYPE_TEXT,TYPE_BOOL]
    }
BOOL_OPERATIONS = ['plus petit que','plus grand que','plus petit ou egal que','plus grand ou egal que','est egal a']

def return_type_var(var_name):
    if var_type.__contains__(var_name):
        return var_type[var_name]
    else:
        print("Undefined variable")
        sys.exit(-1)

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
            print("Undefined type")
            sys.exit(-1)
    else:
        try:
            int(self.tok)
            return TYPE_INT
        except:
            regex = re.compile(r'[a-zA-Z]+')
            if regex.match(self.tok) != None:
                return TYPE_VAR
            else:
                print("Illegal variable name")
                sys.exit(-1)
    
@addToClass(AST.OpNode)
def execute(self):

    if len(self.children) == 1:
        type1 = self.children[0].execute()
        if type1 == TYPE_INT or type1 == TYPE_DOUBLE:
            return type1;
        else:
            print("Unary operator not compatible with this type")
            sys.exit(-1)   

    type1 = self.children[0].execute()
    type2 = self.children[1].execute()
    if type1 == TYPE_VAR:
        type1 = return_type_var(type1)
    if type2 == TYPE_VAR:
        type2 = return_type_var(type2)
    
    if type1 in OPERATION_TYPE[self.type] and type2 in OPERATION_TYPE[self.type]:
        if type1 == type2:
            if self.type in BOOL_OPERATIONS:
                return TYPE_BOOL
            else:
                return type1
        elif type1 == TYPE_DOUBLE and type2 == TYPE_INT or type2 == TYPE_DOUBLE and type1 == TYPE_INT:
            if self.type in BOOL_OPERATIONS:
                return TYPE_BOOL
            else:
                return TYPE_DOUBLE
        else:
            print("Variables are not compatible")
            sys.exit(-1)  
    else:
        print("Incompatible type with operator")
        sys.exit(-1)

@addToClass(AST.AssignNode)
def execute(self):
    left_exp_type = None
    right_exp_type = None
    if len(self.children) == 2:
        if self.children[0].execute()==TYPE_VAR:
            left_exp_type = return_type_var(self.children[0].tok)
            right_exp_type = self.children[1].execute()
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

@addToClass(AST.WhileNode)
@addToClass(AST.IfNode)
def execute(self):
    if self.children[0].execute() != TYPE_BOOL:
        print("Condition expression has to be bool")
        sys.exit(-1)
    for c in self.children:
        c.execute()
    
@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.PrintNode)
def execute(self):
    print("PRINTNODE")
    type1 = self.children[0].execute()
    if type1 == TYPE_VAR:
        return_type_var(type1)

@addToClass(AST.ForNode)
def execute(self):
    print("POUR" ,self)
    
    
if __name__ == "__main__":
    import os
    test_dir = "./tests/semantic/"
    try:
        prog = "SI(2 est egal a 3){ afficher 2;};afficher 3;"
        #prog = "POUR(i de 1 a 10 par pas de 1){ afficher i;};"
        execute(parse(prog))
    except:
        pass
    """for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        print(file)
        print("----------------------")
        result = parse(prog)
        execute(result)"""