from enum import Enum
from bparser import BParser
from intbase import InterpreterBase, ErrorType
from typing import List
import copy

# TEST


def read_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


program_source = read_file('parsing.txt')


class Intepreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

    def run(self):
        result, parsed_program = BParser.parse(program_source)
        print(parsed_program)


if __name__ == '__main__':
    Intepreter = Intepreter()
    Intepreter.run()
    pass
