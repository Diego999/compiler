import AST
import sys
from AST import addToClass
from parser_2 import parse
from semantic_3 import BOOL_TRUE, BOOL_FALSE
before = ['public class main', '{', '\tpublic static void main(String[] args)', '\t{']
after = ['\t}', '}']

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
def execute(self, prefix=''):
    if self.tok[0] == '"' and self.tok[-1] == '"':
        out = self.tok[1:-1]
        for e in to_escape:
            out.replace(e, '\\' + e)
        return prefix + '"' + out + '"'
    elif self.tok == BOOL_TRUE or self.tok == BOOL_FALSE:
        return prefix + self.tok
    elif self.tok.find(',') != -1:
        return prefix + self.tok.replace(',', '.')
    return prefix + self.tok

@addToClass(AST.OpNode)
def execute(self, prefix=''):
    if len(self.children) == 1:
        return prefix + '(' + var_equivalence[self.type] + '(' + self.children[0].execute() + ')' + ')'
    elif len(self.children) == 2:
        left = self.children[0].execute()
        right = self.children[1].execute()
        return prefix + left + var_equivalence[self.type] + right


@addToClass(AST.AssignNode)
def execute(self, prefix=''):
    if len(self.children) == 2:
        return prefix + self.children[0].tok + ' ' + var_equivalence[self.type] + ' ' + self.children[1].execute() + ';'
    elif len(self.children) == 3:
        return prefix + var_equivalence[self.children[1].tok] + ' ' + self.children[0].tok + ' ' + var_equivalence[self.type] + ' ' + self.children[2].execute() + ';'


@addToClass(AST.WhileNode)
def execute(self, prefix=''):
    return prefix + 'while (' + self.children[0].execute() + ')\n' + prefix + '{\n' + self.children[1].execute(prefix) + prefix + '}'


@addToClass(AST.IfNode)
def execute(self, prefix=''):
    out = 'if (' + self.children[0].execute('') + ')\n' + prefix + '{\n' + self.children[1].execute(prefix) + prefix + '}'
    if len(self.children) == 3:
        out += '\n' + prefix + 'else\n' + prefix + '{\n' + self.children[2].execute(prefix) + prefix + '}'
    return prefix + out


@addToClass(AST.ForNode)
def execute(self, prefix=''):
    return prefix + 'for(' + self.children[0].execute('')[:-1] + ';' + self.children[1].children[0].execute('') + '; ' + self.children[2].execute('')[:-1] + ')\n' + prefix + '{\n' + self.children[1].children[1].execute(prefix) + prefix + '}'


@addToClass(AST.ProgramNode)
def execute(self, prefix=''):
    output = ''
    for c in self.children:
        output += c.execute(prefix + '\t') + '\n'
    return output

@addToClass(AST.PrintNode)
def execute(self, prefix=''):
    return prefix + 'System.out.println(' + self.children[0].execute() + ');'


def generate(result):
    out = ''
    for b in before:
        out += b + '\n'
    out += result.execute('\t')
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
