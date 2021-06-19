import sys
import copy


class Line:
    def __init__(self, cir, elements, pins):  # lines, pins: list
        self.elements = copy.deepcopy(elements)
        self.pins = copy.deepcopy(pins)
        self.resistance = 0.0
        for e in elements:
            if cir[e]['type'] == 'structure':
                self.resistance += cir[e]['object'].resistance
            else:
                self.resistance += cir[e]['resistance']

    def reconstruct(self, data, V, I):
        res = []
        for i in self.elements:
            if data[i]['type'] == 'structure':
                rx = data[i]['object'].resistance
            else:
                rx = data[i]['resistance']

            res.append((i, V * rx / self.resistance, I))
        return res


class Parallel:
    def __init__(self, cir, lines):
        self.lines = copy.deepcopy(lines)
        self.admittance = 0
        for l in lines:
            if cir[l]['type'] == 'structure':
                self.admittance += 1.0 / cir[l]['object'].resistance
            else:
                self.admittance += 1.0 / cir[l]['resistance']
        if self.admittance:
            self.resistance = 1.0 / self.admittance
        else:
            sys.exit()

    def reconstruct(self, data, V, I):
        res = []
        for i in self.lines:
            if data[i]['type'] == 'structure':
                rx = data[i]['object'].resistance
            else:
                rx = data[i]['resistance']

            res.append((i, V, V / rx))
        return res


class Bridge:
    def __init__(self, cir, lines, pins):
        self.lines = tuple(copy.deepcopy(lines))
        self.pins = copy.deepcopy(pins)
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

    def reconstruct(self, data, V, I):
        res = []
        vl = [0 for _ in range(5)]

        #  4, 1, 3변환 -> 0, 2 전압
        tempV = V * (1 - ((self.rl[1] * self.rl[3]) / (self.rl[1] + self.rl[3] + self.rl[4])) / self.resistance)
        vl[0] = tempV * self.rl[0] / (self.rl[0] + (self.rl[1] * self.rl[4]) / (self.rl[1] + self.rl[3] + self.rl[4]))
        vl[2] = tempV * self.rl[2] / (self.rl[2] + (self.rl[3] * self.rl[4]) / (self.rl[1] + self.rl[3] + self.rl[4]))

        tempV = V * (1 - ((self.rl[0] * self.rl[2]) / (self.rl[0] + self.rl[2] + self.rl[4])) / self.resistance)
        vl[1] = tempV * self.rl[1] / (self.rl[1] + (self.rl[0] * self.rl[4]) / (self.rl[0] + self.rl[2] + self.rl[4]))
        vl[3] = tempV * self.rl[3] / (self.rl[3] + (self.rl[2] * self.rl[4]) / (self.rl[0] + self.rl[2] + self.rl[4]))

        rth = 1 / (1 / self.rl[0] + 1 / self.rl[1]) + 1 / (1 / self.rl[2] + 1 / self.rl[3])
        vth = V * (self.rl[0] / (self.rl[0] + self.rl[1]) - self.rl[2] / (self.rl[2] + self.rl[3]))
        i = vth / (rth + self.rl[4])
        vl[4] = i * self.rl[4]

        for n in range(5):
            res.append((self.lines[n], vl[n], vl[n] / self.rl[n]))

        return res
