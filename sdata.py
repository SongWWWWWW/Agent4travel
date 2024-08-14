from typing import List, Tuple


class SData:  # Single data
    def __init__(self, path: str, instruction: str = None):
        self.path: List[Tuple] = self.parse_data(path)
        self.instruction = instruction

    def parse_data(self, path) -> List[Tuple]:
        p = path.split(';')
        new = []
        for i in range(len(p)):
            s = p[i].split(',')
            new.append((eval(s[1]), eval(s[0])))
        return new
    def __str__(self):
        s = "Path: \033[91m" + str(self.path[0]).strip("(").strip(")") + "\033[0m->...->\033[91m" + str(self.path[-1]).strip("(").strip(")") + "\033[0m Instruction: " + (self.instruction if self.instruction is not None else "None")
        return s