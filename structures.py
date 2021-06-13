import sys


class Line:
    def __init__(self, cir, elements, pins):  # lines, pins: list
        self.elements = elements
        self.pins = pins
        self.resistance = 0.0
        print(elements)
        for e in elements:
            if cir[e]['type'] == 'structure':
                self.resistance += cir[e]['object'].resistance
            else:
                print(f'cir: {cir}\nele: {e}\npin: {pins}')
                self.resistance += cir[e]['resistance']


class Parallel:
    def __init__(self, cir, lines):
        self.lines = lines
        self.admittance = 0
        print(f'l: {lines}')
        for l in lines:
            if cir[l]['type'] == 'structure':
                print(f's: {l}')
                self.admittance += 1.0 / cir[l]['object'].resistance
            else:
                print(f'e: {l}')
                print(f'c: {cir}')
                self.admittance += 1.0 / cir[l]['resistance']
        if self.admittance:
            self.resistance = 1.0 / self.admittance
        else:
            print('ERR: Admittance is 0')
            sys.exit()


class Bridge:
    def __init__(self, cir, lines, pins):
        self.lines = lines
        self.pins = pins
        self.rl = []
        for l in self.lines:
            if cir[l]['type'] == 'structure':
                self.rl.append(cir[l]['object'].resistance)
            else:
                self.rl.append(cir[l]['resistance'])
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
