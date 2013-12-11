import AST
import sys
from AST import addToClass
from parser_2 import parse
from semantic_3 import BOOL_TRUE, BOOL_FALSE
before = ['public class main', '{', 'public static void main(String[] args)', '{']
after = ['}', '}']

var_equivalence = {
    'texte': 'String',
    'entier': 'int',
    'reel': 'double',
    'booleen': 'boolean',
    'plus': '+',
    'moins': '-',
    'divise par': '/',
    'fois': '*',
    'plus petit que': '<',
    'plus grand que': '>',
    'plus petit ou egal que': '<=',
    'plus grand ou egal que': '>=',
    'est egal a': '==',
    'egal': '=',
    'vrai': 'true',
    'faux': 'false'
}

to_escape = ['\\', '\'', '"']

@addToClass(AST.TokenNode)
def execute(self):
    if self.tok[0] == '"' and self.tok[-1] == '"':
        out = self.tok[1:-1]
        for e in to_escape:
            out.replace(e, '\\' + e)
        return '"' + out + '"'
    elif self.tok == BOOL_TRUE or self.tok == BOOL_FALSE:
        return var_equivalence[self.tok]
    elif self.tok.find(',') != -1:
        return self.tok.replace(',', '.')
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    if len(self.children) == 1:
        return '(' + var_equivalence[self.type] + '(' + self.children[0].execute() + ')' + ')'
    elif len(self.children) == 2:
        left = self.children[0].execute()
        right = self.children[1].execute()
        return left + var_equivalence[self.type] + right


@addToClass(AST.AssignNode)
def execute(self):
    if len(self.children) == 2:
        return self.children[0].tok + ' ' + var_equivalence[self.type] + ' ' + self.children[1].execute() + ';'
    elif len(self.children) == 3:
        return var_equivalence[self.children[1].tok] + ' ' + self.children[0].tok + ' ' + var_equivalence[self.type] + ' ' + self.children[2].execute() + ';'


@addToClass(AST.WhileNode)
def execute(self):
    return 'while (' + self.children[0].execute() + ')\n{\n' + self.children[1].execute() + '}\n'


@addToClass(AST.IfNode)
def execute(self):
    out = 'if (' + self.children[0].execute() + ')\n{\n' + self.children[1].execute() + '}\n'
    if len(self.children) == 3:
        out += 'else\n{\n' + self.children[2].execute() + '}\n'
    return out


@addToClass(AST.ForNode)
def execute(self):
    return 'for(' + self.children[0].execute()[:-1] + ';' + self.children[1].children[0].execute() + '; ' + self.children[2].execute()[:-1] + ')\n{\n' + self.children[1].children[1].execute() + '}\n'


@addToClass(AST.ProgramNode)
def execute(self):
    output = ''
    for c in self.children:
        output += c.execute() + '\n'
    return output

@addToClass(AST.PrintNode)
def execute(self):
    return 'System.out.println(' + self.children[0].execute() + ');'


def generate(result):
    out = ''
    for b in before:
        out += b + '\n'
    out += result.execute()
    for a in after:
        out += a + '\n'
    return out

if __name__ == "__main__":
    import os
    test_dir = "./tests/generator/"
    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        print(file)
        print("----------------------")
        result = parse(prog)
        print(generate(result))
