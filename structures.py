class Line:
    def __init__(self, elements, pins):  # lines, pins: list
        self.elements = elements
        self.pins = pins
        self.resistance = 0.0
        for i in elements:
            if 'resistance' in i:
                self.resistance += i['resistance']


class Parallel:
    def __init__(self, lines):
        self.lines = lines
        self.admittance = 0
        for i in lines:
            if str(type(i)) == "<class 'dict'>":
                self.admittance += 1.0/i['resistance']
            else:
                self.admittance += 1.0/i.resistance
        self.resistance = 1.0/self.admittance


class Bridge:
    def __init__(self, lines, pins):
        self.lines = lines
        self.pins = pins
        self.rl = []
        for i in self.lines:
            if str(type(i)) == "<class 'dict'>":
                self.rl.append(i['resistance'])
            else:
                self.rl.append(i.resistance)
        self.resistance = (1 / (
            1 / (
                self.rl[0] +
                ((self.rl[1] * self.rl[4]) /
                 (self.rl[1] + self.rl[3] + self.rl[4]))
            ) +
            1 / (
                self.rl[2] +
                ((self.rl[3] * self.rl[4]) /
                 (self.rl[1] + self.rl[3] + self.rl[4]))
            )
        ) +
            ((self.rl[1] * self.rl[3]) /
             (self.rl[1] + self.rl[3] + self.rl[4]))
        )
