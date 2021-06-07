import json
import sys
import copy
import itertools
import structures as s


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
    while True:
        res, cir = findLine(cir, matrix, pinList)
        if res:
            matrix, pinList = getAdMatrix(cir)
        else:
            break


def findConnected(matrix, pin):
    connected = [pin]
    start = True
    for i in range(len(matrix[pin])):
        if matrix[pin][i] == 1:
            connected.append(i)
            if sum(matrix[i]) == 2:
                connected += findConnected(matrix, i)
    for i in range(len(connected)):
        if sum(matrix[i]) != 2:
            if start:
                connected[i], connected[0] = connected[0], connected[i]
                start = False
            else:
                connected[i], connected[-1] = connected[-1], connected[i]
    for i in range(len(connected)):
        for j in range(i+1, len(connected)):
            if matrix[i][j] == 1:
                connected[i+1], connected[j] = connected[j], connected[i+1]
    endPins = [connected[0], connected[-1]]
    del connected[0]
    del connected[-1]
    return connected, endPins


def findLine(cir, matrix, pinList):
    '''
    Replace elements in cir into Line object
    return False when there is no more Line
    '''
    connected = None
    elements = []
    endPins = []
    for i in range(len(pinList)):
        if (sum(matrix[i]) == 2) and (2 not in matrix[i]):
            connected, endPins = findConnected(matrix, i)
            if len(connected) == 1:
                for j in endPins:
                    for k in cir:
                        if (pinList[j] in cir[k]['pin'] and
                           pinList[connected[0]] in cir[k]['pin']):
                            elements.append(k)
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
    if connected is not None:
        endPins = [pinList[n] for n in endPins]
        connected = [pinList[n] for n in connected]
        for i in connected:
            removeElements = []
            for j in cir:
                if i in cir[j]['pin']:
                    removeElements.append(j)
            for _ in removeElements:
                cir.pop(removeElements.pop())
        cir[f'Line{numLine}'] = {
                                 'type': 'Line',
                                 'obJect': s.Line(elements, connected),
                                 'pin': endPins}
        pinList = [n for n in pinList if n not in connected]
        return True, cir
    else:
        return False, cir


# def findParallel(bM, bE, seq, parallel):
#     isEnd = True
#     parallel.append(list())
#     pinComb = itertools.combinations(bE, 2)
#     for i in pinComb:
#         x, y = bE.index(i[0]), bE.index(i[1])
#         if bM[x][y] >= 2:
#             print(bM, bE, seq, bM[x][y], x, y)
#             # seq겹 병렬을 병렬[]의 seq번째 리스트에 ((핀, 핀), connection수)로 저장
#             parallel[seq].append(((bE[x], bE[y]), bM[x][y]))
#             bM[x][y] = 1  # seq겹 병렬 무시
#             isEnd = False
#     if isEnd:
#         parallel.pop()
#         return((bM, parallel))
#     else:
#         basicMatrix = getBasicMatrix(bM, bE)
#         print('.')
#         return(findParallel(basicMatrix[0], basicMatrix[1], seq + 1, parallel))
def findParallel(cir, matrix, pinList):
    lines = []
    found = False
    for i in range(len(pinList)):
        for j in range(i+1, len(pinList)):
            if matrix[i, j] >= 2:
                for k in cir:
                    if i in cir[k]['pin'] and j in cir[k]['pin']:
                        lines.append(k)
                found = True
            if found:
                break
        if found:
            break
    if lines:
        
            

def findBridge():
    isEnd = True

# =================================================================================

with open(sys.argv[1], 'r') as f:
    circuit = json.load(f)
editCircuit = copy.deepcopy(circuit)

structureCircuit(editCircuit)
print(editCircuit)
