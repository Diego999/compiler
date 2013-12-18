from lex_1 import generate_lex
from parser_2 import generate_parser
from semantic_3 import generate_semantic
from generator_4 import generate_output

if __name__ == "__main__":
    import os
    test_dir = "./tests/compiling/"
    for file in os.listdir(test_dir):
        prog = open(test_dir+file).read()
        if generate_lex(prog, file.split(".")[0]) != 0:
            continue
        (error_number, result) = generate_parser(prog, file.split(".")[0])
        if error_number != 0:
            continue

        if generate_semantic(result, file.split(".")[0]) != 0:
            continue

        generate_output(result, file.split('.')[0])