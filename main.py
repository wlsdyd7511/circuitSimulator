import json
import sys
import copy

trackPoint = str()
trackElement = str()


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
                if (pinList[i] in cir[k]["pin"]) and (pinList[j] in cir[k]["pin"]):
                    cnt += 1
                    matrix[i][j] = cnt
    # print(matrix)
    return((matrix, pinList))


def getBasicMatrix(matrix, pinList):
    basicMatrix = copy.deepcopy(matrix)
    basicElements = [pin for pin in pinList]
    numPin = len(pinList)
    pinToDel = list()
    for i in range(numPin):
        cntPin = 0
        for j in range(numPin):
            cntPin += matrix[i][j]
        if cntPin == 2:
            pinToDel.append(i)
            pinToConnect = list()
            for j in range(numPin):
                if matrix[i][j] == 1:
                    pinToConnect.append(j)
            basicMatrix[pinToConnect[0]][pinToConnect[1]] += 1
            basicMatrix[pinToConnect[1]][pinToConnect[0]] += 1

    pinToDel.reverse()
    cntSeq = 0
    for i in pinToDel:
        del basicElements[i]
        del basicMatrix[i]
        cntSeq += 1
        for j in range(numPin - cntSeq):
            del basicMatrix[j][i]
    return((basicMatrix, basicElements))


# basicMatrix, basicElements, seq = 0, parallel = list()
def findParallel(bM, bE, seq, parallel):
    endCheck = 1
    parallel.append(list())
    for i in range(len(bM)):
        for j in range(len(bM)):
            if bM[i][j] >= 2:
                print(bM, bE, seq, bM[i][j], i, j)
                # seq겹 병렬을 병렬[]의 seq번째 리스트에 ((핀, 핀), connection수)로 저장
                parallel[seq].append(
                    ((bE[i], bE[j]), bM[i][j]))
                bM[i][j] = 1  # seq겹 병렬 무시
                endCheck = 0
                # print(endCheck)
    if endCheck == 1:
        parallel.pop()
        return((bM, parallel))
    else:
        basicMatrix = getBasicMatrix(bM, bE)
        print('.')
        return(findParallel(basicMatrix[0], basicMatrix[1], seq + 1, parallel))


with open(sys.argv[1], 'r') as f:
    circuit = json.load(f)
# print(circuit)
editCircuit = copy.deepcopy(circuit)
# circuitOut = json.dumps(circuit, indent = 4)
# print(circuitOut)
# print(type(circuitOut))

for i in circuit:
    # print(circuit[i])
    if(circuit[i]['type'] == 'DCPower'):
        editCircuit[circuit[i]['pin'][0]] = dict()
        editCircuit[circuit[i]['pin'][0]][circuit[i]
                                          ['pin'][1]] = circuit[i]['voltage']
        trackPoint = circuit[i]['pin'][1]
        trackElement = i


ADMatrix = getAdMatrix(circuit)
# print(editCircuit)
print(ADMatrix)
basicMatrix = getBasicMatrix(ADMatrix[0], ADMatrix[1])
print(basicMatrix)
superBasicMatrix = findParallel(basicMatrix[0], basicMatrix[1], 0, [])
print(superBasicMatrix)
