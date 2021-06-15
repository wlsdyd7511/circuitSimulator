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
    pinList = []
    for k in cir:
        for pin in cir[k]["pin"]:
            if pin not in pinList:
                pinList.append(pin)
    # pinList.sort()
    numPin = len(pinList)
    matrix = [[0 for _ in range(numPin)] for _ in range(numPin)]
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
            if res:
                noStructureCount = 0
                matrix, pinList = getAdMatrix(cir)
            else:
                noStructureCount += 1
                nextFind = 1
            print(f'count(l): {noStructureCount}')
        elif nextFind == 1:
            res, cir = findParallel(cir, matrix, pinList)
            if res:
                noStructureCount = 0
                matrix, pinList = getAdMatrix(cir)
            else:
                noStructureCount += 1
                nextFind = 2
            print(f'count(p): {noStructureCount}')
        elif nextFind == 2:
            res, cir = findBridge(cir, matrix, pinList)
            if res:
                noStructureCount = 0
                matrix, pinList = getAdMatrix(cir)
            else:
                noStructureCount += 1
                nextFind = 0
            print(f'count(b): {noStructureCount}')


def findConnected(cir, matrix, pinList, pin, doSort):
    connected = [pin]
    BTConnected = False
    for k in cir:
        if pinList[pin] in cir[k]['pin'] and cir[k]['type'] == 'DCPower':
            BTConnected = True
    start = True
    for i in range(len(matrix[pin])):
        if matrix[pin][i] == 1:
            (f'i: {i}')
            connected.append(i)
            if sum(matrix[i]) == 2 and not BTConnected:
                iConnected, _ = findConnected(cir, matrix, pinList, i, False)
                connected += iConnected

    if doSort:
        (f'Before remove overlap: {connected}')
        connected = list(set(connected))  # 정렬 전에 중복 제거
        (f'After remove overlap: {connected}')

        for i in range(len(connected)):  # 정렬
            currentBTConnected = False
            for k in cir:
                (f'currentElement: {k}')
                (f'connected: {connected}')
                if pinList[connected[i]] in cir[k]['pin'] and cir[k]['type'] == 'DCPower':
                    currentBTConnected = True
            if sum(matrix[connected[i]]) != 2 or currentBTConnected:
                if start:
                    connected[i], connected[0] = connected[0], connected[i]
                    start = False
                else:
                    connected[i], connected[-1] = connected[-1], connected[i]
        (f'after sort1: {[pinList[n] for n in connected]}')
        for i in range(len(connected) - 1):
            for j in range(i + 1, len(connected) - 1):
                if matrix[i][j] == 1:
                    connected[i + 1], connected[j] = connected[j], connected[i + 1]
        (f'after sort2: {[pinList[n] for n in connected]}')
        if matrix[connected[-1]][connected[-2]] != 1:
            ('ERR: cannot sort line')
    endPins = [connected[0], connected[-1]]
    del connected[0]
    del connected[-1]
    return connected, endPins


def findLine(cir, matrix, pinList):
    '''
    Replace elements in cir into Line object
    return False when there is no more Line
    '''
    global numLine
    global restore
    for i in range(len(pinList)):
        connected = None
        elements = []
        endPins = []
        iDCPower = False
        for k in cir:
            if cir[k]['type'] == 'DCPower' and pinList[i] in cir[k]['pin']:
                iDCPower = True
        (f'iDCPower: {iDCPower}')
        if sum(matrix[i]) == 2 and 2 not in matrix[i] and not iDCPower:
            (f'searchPin: {pinList[i]}')
            connected, endPins = findConnected(cir, matrix, pinList, i, True)
            if len(connected) == 1:
                ('1 pin in connected')
                (f'endPins: {endPins}')
                for j in endPins:
                    for k in cir:
                        (pinList[i], pinList[j])
                        if (pinList[j] in cir[k]['pin'] and
                           pinList[connected[0]] in cir[k]['pin']):
                            elements.append(k)
            else:
                ('many pins in connected')
                for k in cir:
                    if (pinList[connected[0]] in cir[k]['pin'] and
                       pinList[connected[1]] not in cir[k]['pin']):
                        elements.append(k)
                for j in range(len(connected) - 1):
                    for k in cir:
                        if (pinList[connected[i]] in cir[k]['pin'] and
                           pinList[connected[i + 1]] in cir[k]['pin']):
                            elements.append(k)
                for j in cir:
                    if (pinList[connected[-1]] in cir[j]['pin'] and
                       pinList[connected[-2]] not in cir[j]['pin']):
                        elements.append(k)
                break
            (f'elements: {elements}')
    if connected is not None:
        (f'connected: {connected}\nelements: {elements}')
        endPins = [pinList[n] for n in endPins]
        connected = [pinList[n] for n in connected]
        cir[f'Line{numLine}'] = {
            'type': 'structure',
            'structure': 'Line',
            'object': s.Line(cir, elements, connected),
            'pin': endPins}
        for i in connected:
            removeElements = []
            for j in cir:
                if i in cir[j]['pin']:
                    removeElements.append(j)
            for _ in range(len(removeElements)):
                temp = removeElements.pop()
                if temp not in restore:
                    restore[temp] = copy.deepcopy(cir[temp])
                cir.pop(temp)
        numLine += 1
        pinList = [n for n in pinList if n not in connected]
        return True, cir
    else:
        return False, cir


def findParallel(cir, matrix, pinList):
    global numParallel
    global restore
    (cir)
    (matrix)
    (pinList)
    lines = []
    found = False
    pins = []
    for i in range(len(pinList)):
        for j in range(i + 1, len(pinList)):
            if matrix[i][j] >= 2:
                (i, j)
                pins = [pinList[i], pinList[j]]
                for k in cir:
                    if pinList[i] in cir[k]['pin'] and pinList[j] in cir[k]['pin'] and cir[k]['type'] != 'DCPower':
                        lines.append(k)
                (lines)
                if len(lines) >= 2:
                    found = True
                else:
                    found = False
                    lines = []
                    pins = []
            if found:
                break
        if found:
            break
    if found:
        (f'parLines: {lines}')
        cir[f'Parallel{numParallel}'] = {
            'type': 'structure',
            'structure': 'Parallel',
            'object': s.Parallel(cir, lines),
            'pin': pins}
        length = len(lines)
        for _ in range(length):
            temp = lines.pop()
            if temp not in restore:
                restore[temp] = copy.deepcopy(cir[temp])
            cir.pop(temp)
        numParallel += 1
    return found, cir


def findBridge(cir, matrix, pinList):
    global numBridge
    global restore
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

        for (m, e) in pair:
            for k in cir:
                if m in cir[k]['pin'] and e in cir[k]['pin']:
                    lines.append(k)

        for k in cir:
            if m[0] in cir[k]['pin'] and m[1] in cir[k]['pin']:
                lines.append(k)

        cir[f'bridge{numBridge}'] = {
            'type': 'structure',
            'structure': 'Bridge',
            'object': s.Bridge(lines, midPins),
            'pin': endPins}

        for _ in range(5):
            temp = lines.pop()
            if temp not in restore:
                restore[temp] = copy.deepcopy(cir[temp])
            cir.pop(temp)

    return found, cir


# =================================================================================

with open(sys.argv[1], 'r') as f:
    circuit = json.load(f)
editCircuit = copy.deepcopy(circuit)
restore = copy.deepcopy(circuit)

structureCircuit(editCircuit)
(editCircuit)
