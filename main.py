import sys
import copy
import structures as s
from itertools import combinations, product


numLine = 1
numParallel = 1
numBridge = 1

restore = None
editCircuit = None


def getAdMatrix(cir):
    pinList = []
    for k in cir:
        for pin in cir[k]["pin"]:
            if pin not in pinList:
                pinList.append(pin)
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
        elif nextFind == 1:
            res, cir = findParallel(cir, matrix, pinList)
            if res:
                noStructureCount = 0
                matrix, pinList = getAdMatrix(cir)
            else:
                noStructureCount += 1
                nextFind = 2
        elif nextFind == 2:
            res, cir = findBridge(cir, matrix, pinList)
            if res:
                noStructureCount = 0
                matrix, pinList = getAdMatrix(cir)
            else:
                noStructureCount += 1
                nextFind = 0


def findConnected(cir, matrix, pinList, pin, doSort):
    connected = [pin]
    endPins = []
    start = True
    for i in range(len(matrix[pin])):
        BTConnected = False
        for k in cir:
            if pinList[i] in cir[k]['pin'] and cir[k]['type'] == 'DCPower':
                BTConnected = True
        if matrix[pin][i] == 1:
            connected.append(i)
            if sum(matrix[i]) == 2 and not BTConnected:
                iConnected, _ = findConnected(cir, matrix, pinList, i, False)
                connected += iConnected

    if doSort:
        connected = list(set(connected))  # 정렬 전에 중복 제거
        for i in range(len(connected)):  # 정렬
            currentBTConnected = False
            for k in cir:
                if pinList[connected[i]] in cir[k]['pin'] and cir[k]['type'] == 'DCPower':
                    currentBTConnected = True
            if sum(matrix[connected[i]]) != 2 or currentBTConnected:
                if start:
                    connected[i], connected[0] = connected[0], connected[i]
                    start = False
                else:
                    connected[i], connected[-1] = connected[-1], connected[i]
        for i in range(len(connected) - 1):
            for j in range(i + 1, len(connected) - 1):
                if matrix[i][j] == 1:
                    connected[i + 1], connected[j] = connected[j], connected[i + 1]
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

    found = False

    for i in range(len(pinList)):
        connected = None
        elements = []
        endPins = []
        iDCPower = False
        for k in cir:
            if cir[k]['type'] == 'DCPower' and pinList[i] in cir[k]['pin']:
                iDCPower = True
        if sum(matrix[i]) == 2 and 2 not in matrix[i] and not iDCPower:
            connected, endPins = findConnected(cir, matrix, pinList, i, True)
            if len(connected) == 1:
                for j in endPins:
                    for k in cir:
                        if (pinList[j] in cir[k]['pin'] and
                           pinList[connected[0]] in cir[k]['pin']):
                            elements.append(k)
                found = True
            else:
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
                found = True
                break
            if found:
                break
    if connected is not None:
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
    lines = []
    found = False
    pins = []
    for i in range(len(pinList)):
        for j in range(i + 1, len(pinList)):
            if matrix[i][j] >= 2:
                pins = [pinList[i], pinList[j]]
                for k in cir:
                    if pinList[i] in cir[k]['pin'] and pinList[j] in cir[k]['pin'] and cir[k]['type'] != 'DCPower':
                        lines.append(k)
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
        cir[f'Parallel{numParallel}'] = {
            'type': 'structure',
            'structure': 'Parallel',
            'object': s.Parallel(cir, lines),
            'pin': pins}
        numParallel += 1
        length = len(lines)
        for _ in range(length):
            temp = lines.pop()
            if temp not in restore:
                restore[temp] = copy.deepcopy(cir[temp])
            cir.pop(temp)
    return found, cir


def findBridge(cir, matrix, pinList):
    global numBridge
    global restore
    lines = []
    found = False
    comb = list(combinations(range(len(pinList)), 4))
    endPins = []
    midPins = []
    for c in comb:
        ends = list(combinations(c, 2))
        for e in ends:
            eBTConnected = False
            for k in cir:
                if pinList[e[0]] in cir[k]['pin'] and pinList[e[1]] in cir[k]['pin'] and cir[k]['type'] == 'DCPower':
                    eBTConnected = True
            if matrix[e[0]][e[1]] == 0 or eBTConnected:
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
            break
    if found:
        pair = product(midPins, endPins)

        for (m, e) in pair:
            for k in cir:
                if pinList[m] in cir[k]['pin'] and pinList[e] in cir[k]['pin']:
                    lines.append(k)

        for k in cir:
            if pinList[midPins[0]] in cir[k]['pin'] and pinList[midPins[1]] in cir[k]['pin']:
                lines.append(k)

        midPins = [pinList[n] for n in midPins]
        endPins = [pinList[n] for n in endPins]

        cir[f'bridge{numBridge}'] = {
            'type': 'structure',
            'structure': 'Bridge',
            'object': s.Bridge(cir, lines, midPins),
            'pin': endPins}
        numBridge += 1

        for _ in range(5):
            temp = lines.pop()
            if temp not in restore:
                restore[temp] = copy.deepcopy(cir[temp])
            cir.pop(temp)

    return found, cir


# =================================================================================

def analyze(cir, data):
    end = True
    for k in cir:
        if cir[k]['type'] == 'structure':
            end = False
            remove = k
            temp = cir[k]['object'].reconstruct(data, cir[k]['V'], cir[k]['I'])
            break

    if not end:
        del cir[remove]
        for (name, V, I) in temp:
            cir[name] = copy.deepcopy(data[name])
            cir[name]['V'] = V
            cir[name]['I'] = I

    return end, cir


# =================================================================================

# with open(sys.argv[1], 'r') as f:
#     circuit = json.load(f)

def rawToResult(circuit):
    global editCircuit
    global restore

    editCircuit = copy.deepcopy(circuit)
    restore = copy.deepcopy(circuit)

    structureCircuit(editCircuit)

    if len(editCircuit) != 2:
        print('ERROR: 분석할 수 없는 회로입니다.')
        sys.exit()

    for k in editCircuit:
        if editCircuit[k]['type'] == 'DCPower':
            entireVolt = editCircuit[k]['voltage']
        else:
            notPower = k
    editCircuit[notPower]['V'] = entireVolt
    if editCircuit[notPower]['type'] == 'structure':
        tempR = editCircuit[notPower]['object'].resistance
    else:
        tempR = editCircuit[notPower]['resistance']
    editCircuit[notPower]['I'] = entireVolt / tempR

    end = False

    while not end:
        end, editCircuit = analyze(editCircuit, restore)

    return editCircuit
