import json
import sys
import copy
import itertools
import structures as s
from itertools import combinations, product


numLine = 1
numParallel = 1
numBridge = 1


def getAdMatrix(cir):
    pinList = list()
    for k in cir:
        for pin in cir[k]["pin"]:
            if pin not in pinList:
                pinList.append(pin)
    pinList.sort()
    numPin = len(pinList)
    matrix = [[0 for i in range(numPin)] for j in range(numPin)]
    for i in range(numPin):
        for j in range(numPin):
            cnt = 0
            if i == j:
                continue
            for k in cir:
                if ((pinList[i] in cir[k]["pin"]) and (pinList[j] in cir[k]["pin"])):
                    cnt += 1
                    matrix[i][j] = cnt
    return matrix, pinList


def structureCircuit(cir):
    matrix, pinList = getAdMatrix(cir)
    noStructureCount = 0
    nextFind = 0  # 0: Line, 1: Parallel, 2: Bridge
    while noStructureCount < 3:
        if nextFind == 0:
            res, cir = findLine(cir, matrix, pinList)
            print(f'line: {res}, {cir}')
            if res:
                noStructureCount = 0
                matrix, pinList = getAdMatrix(cir)
            else:
                noStructureCount += 1
                nextFind = 1
        elif nextFind == 1:
            res, cir = findParallel(cir, matrix, pinList)
            print(f'parallel: {res}, {cir}')
            if res:
                noStructureCount = 0
                matrix, pinList = getAdMatrix(cir)
            else:
                noStructureCount += 1
                nextFind = 2
        elif nextFind == 2:
            res, cir = findBridge(cir, matrix, pinList)
            print(f'bridge: {res}, {cir}')
            if res:
                noStructureCount = 0
                matrix, pinList = getAdMatrix(cir)
            else:
                noStructureCount += 1
        print()


def findConnected(cir, matrix, pin):
    connected = [pin]
    BTConnected = False
    for k in cir:
        if pin in cir[k]['pin'] and cir[k]['type'] == 'DCPower':
            BTConnected = True
    start = True
    for i in range(len(matrix[pin])):
        if matrix[pin][i] == 1:
            connected.append(i)
            if sum(matrix[i]) == 2 and not BTConnected:
                connected += findConnected(cir, matrix, i)
#     print(f'before sort: {connected}')

    for i in range(len(connected)):
        if sum(matrix[connected[i]]) != 2:
            if start:
                connected[i], connected[0] = connected[0], connected[i]
                start = False
            else:
                connected[i], connected[-1] = connected[-1], connected[i]
    for i in range(len(connected)):
        for j in range(i+1, len(connected)):
            if matrix[i][j] == 1:
                connected[i+1], connected[j] = connected[j], connected[i+1]

#     print(f'after sort: {connected}')
    endPins = [connected[0], connected[-1]]
    del connected[0]
    del connected[-1]
    return connected, endPins


def findLine(cir, matrix, pinList):
    '''
    Replace elements in cir into Line object
    return False when there is no more Line
    '''
#     print(f'pl: {pinList}')
#     print(f'mt: {matrix}')
    global numLine
    connected = None
    elements = []
    endPins = []
    for i in range(len(pinList)):
        if (sum(matrix[i]) == 2) and (2 not in matrix[i]):
            connected, endPins = findConnected(cir, matrix, i)
            if len(connected) == 1:
                for j in endPins:
                    for k in cir:
                        if (pinList[j] in cir[k]['pin'] and
                           pinList[connected[0]] in cir[k]['pin']):
                            elements.append(k)
                            print(f'el: {elements}')
                break
            else:
                for j in cir:
                    if (pinList[connected[0]] in cir[j]['pin'] and
                       pinList[connected[1]] not in cir[j]['pin']):
                        elements.append(j)
                for j in range(len(connected)-1):
                    for k in cir:
                        if (pinList[connected[i]] in cir[k]['pin'] and
                           pinList[connected[i+1]] in cir[k]['pin']):
                            elements.append(k)
                for j in cir:
                    if (pinList[connected[-1]] in cir[j]['pin'] and
                       pinList[connected[-2]] not in cir[j]['pin']):
                        elements.append(k)
                break
#     print(f'c: {connected}')
#     print(f'ep: {endPins}')
#     print()
    if connected is not None:
        endPins = [pinList[n] for n in endPins]
        connected = [pinList[n] for n in connected]
        for i in connected:
            removeElements = []
            for j in cir:
                if i in cir[j]['pin']:
                    removeElements.append(j)
            for _ in range(len(removeElements)):
                cir.pop(removeElements.pop())
        cir[f'Line{numLine}'] = {
                                 'type': 'Line',
                                 'obJect': s.Line(elements, connected),
                                 'pin': endPins}
        numLine += 1
        pinList = [n for n in pinList if n not in connected]
        return True, cir
    else:
        return False, cir


def findParallel(cir, matrix, pinList):
    global numParallel
    lines = []
    found = False
    pins = []
    for i in range(len(pinList)):
        for j in range(i+1, len(pinList)):
            if matrix[i][j] >= 2:
                pins = [i, j]
                for k in cir:
                    if i in cir[k]['pin'] and j in cir[k]['pin']:
                        lines.append(k)
                found = True
            if found:
                break
        if found:
            break
    if lines:
        for _ in lines:
            cir.pop(lines.pop())
        cir[f'Parallel{numParallel}'] = {
                                         'type': 'Parallel',
                                         'object': s.Parallel(lines),
                                         'pin': pins}
        numParallel += 1
    return found, cir


def findBridge(cir, matrix, pinList):
    global numBridge
    lines = []
    found = False
    comb = list(combinations(pinList, 4))
    endPins = []
    midPins = []
    for c in comb:
        ends = list(combinations(c, 2))
        for e in ends:
            if matrix[e[0]][e[1]] == 0:
                m = [n for n in c if n not in e]
                if matrix[m[0]][m[1]] == 1:
                    prod = list(product(e, m))
                    for (x, y) in prod:
                        if matrix[x][y] != 1:
                            found = False
                            break
                        else:
                            found = True
                if found:
                    endPins = e
                    midPins = m
                    break
        if found:
            break
    if found:
        pair = product(midPins, endPins)
        for i in cir:
            for j in pair:
                if j[0] in cir[i]['pin'] and j[1] in cir[i]['pin']:
                    cir.pop(j)

        for (m, e) in pair:
            for k in cir:
                if m in cir[k]['pin'] and e in cir[k]['pin']:
                    lines.append(k)

        for k in cir:
            if m[0] in cir[k]['pin'] and m[1] in cir[k]['pin']:
                lines.append(k)

        cir[f'bridge{numBridge}'] = {
                                     'type': 'Bridge',
                                     'object': s.Bridge(lines, midPins),
                                     'pin': endPins}
    return found, cir


# =================================================================================

with open(sys.argv[1], 'r') as f:
    circuit = json.load(f)
editCircuit = copy.deepcopy(circuit)

structureCircuit(editCircuit)
print(editCircuit)
