import AST
import re
from AST import addToClass
from parser_2 import generate_parser

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
    'plus': [TYPE_TEXT, TYPE_INT, TYPE_DOUBLE],
    'moins': [TYPE_INT, TYPE_DOUBLE],
    'divise par': [TYPE_INT, TYPE_DOUBLE],
    'fois': [TYPE_INT, TYPE_DOUBLE],
    'plus petit que': [TYPE_INT, TYPE_DOUBLE],
    'plus grand que': [TYPE_INT, TYPE_DOUBLE],
    'plus petit ou egal que': [TYPE_INT, TYPE_DOUBLE],
    'plus grand ou egal que': [TYPE_INT, TYPE_DOUBLE],
    'est egal a': [TYPE_INT, TYPE_DOUBLE, TYPE_TEXT, TYPE_BOOL]
    }
BOOL_OPERATIONS = ['plus petit que', 'plus grand que', 'plus petit ou egal que', 'plus grand ou egal que', 'est egal a']

error_output = open('outputs/' + 'error_semantic.log', 'w')

def return_type_var(var_name):
    if var_type.__contains__(var_name):
        return var_type[var_name]
    else:
        error_output.write("Undefined variable\n")

@addToClass(AST.TokenNode)
def execute(self):
    if self.tok[0] == '"' and self.tok[-1] == '"':
        return TYPE_TEXT
    elif self.tok == BOOL_TRUE or self.tok == BOOL_FALSE:
        return TYPE_BOOL
    elif self.tok.find(',') != -1:
        try:
            self.tok = self.tok.replace(',', '.')
            float(self.tok)
            return TYPE_DOUBLE
        except:
            error_output.write("Undefined type\n")
    else:
        try:
            int(self.tok)
            return TYPE_INT
        except:
            regex = re.compile(r'[a-zA-Z]+')
            if regex.match(self.tok) is not None:
                return TYPE_VAR
            else:
                error_output.write("Illegal variable name\n")
    
@addToClass(AST.OpNode)
def execute(self):
    if len(self.children) == 1:
        type1 = self.children[0].execute()
        if type1 == TYPE_VAR:
            type1 = return_type_var(self.children[0].tok)
        if type1 == TYPE_INT or type1 == TYPE_DOUBLE:
            return type1
        else:
            error_output.write("Unary operator not compatible with this type\n")

    type1 = self.children[0].execute()
    type2 = self.children[1].execute()
    if type1 == TYPE_VAR:
        type1 = return_type_var(self.children[0].tok)
    if type2 == TYPE_VAR:
        type2 = return_type_var(self.children[1].tok)
    
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
            error_output.write("Variables are not compatible\n")
    else:
        error_output.write("Incompatible type with operator\n")

@addToClass(AST.AssignNode)
def execute(self):
    left_exp_type = None
    right_exp_type = None
    if len(self.children) == 2:
        if self.children[0].execute() == TYPE_VAR:
            left_exp_type = return_type_var(self.children[0].tok)
            right_exp_type = self.children[1].execute()
        else:
            error_output.write("Cannot assign value to a constant\n")
    elif len(self.children) == 3:
        if self.children[0].execute() == TYPE_VAR:
            if var_type.__contains__(self.children[0].tok):
                error_output.write("Duplicate variable\n")
            else:
                var_type[self.children[0].tok] = self.children[1].tok
                left_exp_type = var_type[self.children[0].tok]
            right_exp_type = self.children[2].execute()
    if left_exp_type != right_exp_type:
        error_output.write("Type does not match\n")

@addToClass(AST.WhileNode)
@addToClass(AST.IfNode)
def execute(self):
    if self.children[0].execute() != TYPE_BOOL:
        error_output.write("Condition expression has to be bool\n")
    for c in self.children:
        c.execute()
    
@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.PrintNode)
@addToClass(AST.ForNode)
def execute(self):
    for c in self.children:
        c.execute()


def generate_semantic(prog):
    global var_type
    var_type = {}
    generate_parser(prog).execute()
    error_output.write('\n')

if __name__ == "__main__":
    import os
    test_dir = "./tests/semantic/"
    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        error_output.write('=============='+file+'==============\n')
        generate_semantic(prog)
