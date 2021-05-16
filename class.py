import copy


class Line:
    def __init__(self, elements):
        self.elements = copy.deepcopy(elements)
        self.resistance = 0.0
        for i in elements:
            if 'resistance' in i:
                self.resistance += i['resistance']


class Parallel:
    def __init__(self, lines):
        self.lines = copy.deepcopy(lines)
