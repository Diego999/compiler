import AST
from AST import addToClass
from parser_2 import generate_parser
from semantic_3 import BOOL_TRUE, BOOL_FALSE

before = ['public class Main', '{', '\tpublic static void main(String[] args)', '\t{']
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
def generate(self, prefix=''):
    if self.tok[0] == '"' and self.tok[-1] == '"':
        out = self.tok[1:-1]
        for e in to_escape:
            out = out.replace(e, '\\' + e)
        return prefix + '"' + out + '"'
    elif self.tok == BOOL_TRUE or self.tok == BOOL_FALSE:
        return prefix + var_equivalence[self.tok]
    elif self.tok.find(',') != -1:
        return prefix + self.tok.replace(',', '.')
    return prefix + self.tok

@addToClass(AST.OpNode)
def generate(self, prefix=''):
    if len(self.children) == 1:
        return prefix + '(' + var_equivalence[self.type] + '(' + self.children[0].generate() + ')' + ')'
    elif len(self.children) == 2:
        left = self.children[0].generate()
        right = self.children[1].generate()
        return prefix + left + var_equivalence[self.type] + right


@addToClass(AST.AssignNode)
def generate(self, prefix=''):
    if len(self.children) == 2:
        return prefix + self.children[0].tok + ' ' + var_equivalence[self.type] + ' ' + self.children[1].generate() + ';'
    elif len(self.children) == 3:
        return prefix + var_equivalence[self.children[1].tok] + ' ' + self.children[0].tok + ' ' + var_equivalence[self.type] + ' ' + self.children[2].generate() + ';'


@addToClass(AST.WhileNode)
def generate(self, prefix=''):
    return prefix + 'while (' + self.children[0].generate() + ')\n' + prefix + '{\n' + self.children[1].generate(prefix) + prefix + '}'


@addToClass(AST.IfNode)
def generate(self, prefix=''):
    out = 'if (' + self.children[0].generate('') + ')\n' + prefix + '{\n' + self.children[1].generate(prefix) + prefix + '}'
    if len(self.children) == 3:
        out += '\n' + prefix + 'else\n' + prefix + '{\n' + self.children[2].generate(prefix) + prefix + '}'
    return prefix + out


@addToClass(AST.ForNode)
def generate(self, prefix=''):
    return prefix + 'for(' + self.children[0].generate('')[:-1] + ';' + self.children[1].children[0].generate('') + '; ' + self.children[2].generate('')[:-1] + ')\n' + prefix + '{\n' + self.children[1].children[1].generate(prefix) + prefix + '}'


@addToClass(AST.ProgramNode)
def generate(self, prefix=''):
    output = ''
    for c in self.children:
        output += c.generate(prefix + '\t') + '\n'
    return output

@addToClass(AST.PrintNode)
def generate(self, prefix=''):
    return prefix + 'System.out.println(' + self.children[0].generate() + ');'


def generate_output(result, title):
    with open('outputs/' + title+'.java', 'w') as f:
        out = ''
        for b in before:
            out += b + '\n'
        out += result.generate('\t')
        for a in after:
            out += a + '\n'
        f.write(out)
    return 0

if __name__ == "__main__":
    import os
    test_dir = "./to_compile/"
    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        (err_num, result) = generate_parser(prog, file)
        if result:
             generate_output(result, file.split('.')[0])
