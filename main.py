import json
import sys
import copy
import itertools


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
  return((matrix, pinList))


def getBasicMatrix(matrix, pinList):
  basicMatrix = copy.deepcopy(matrix)
  basicPinList = copy.deepcopy(pinList)
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
    del basicPinList[i]
    del basicMatrix[i]
    cntSeq += 1
    for j in range(numPin - cntSeq):
      del basicMatrix[j][i]
  return((basicMatrix, basicPinList))


# basicMatrix, basicElements, seq = 0, parallel = list()
def findParallel(bM, bE, seq, parallel):
  isEnd = True
  parallel.append(list())
  pinComb = itertools.combinations(bE, 2)
  for i in pinComb:
    x, y = bE.index(i[0]), bE.index(i[1])
    if bM[x][y] >= 2:
      print(bM, bE, seq, bM[x][y], x, y)
      parallel[seq].append(((bE[x], bE[y]), bM[x][y]))# seq겹 병렬을 병렬[]의 seq번째 리스트에 ((핀, 핀), connection수)로 저장
      bM[x][y] = 1# seq겹 병렬 무시
      isEnd = False
  if isEnd == True:
    parallel.pop()
    return((bM, parallel))
  else:
    basicMatrix = getBasicMatrix(bM, bE)
    print('.')
    return(findParallel(basicMatrix[0], basicMatrix[1], seq + 1, parallel))


with open(sys.argv[1], 'r') as f:
  circuit = json.load(f)
editCircuit = copy.deepcopy(circuit)

for i in circuit:
  if(circuit[i]['type'] == 'DCPower'):
    editCircuit[circuit[i]['pin'][0]] = dict()
    editCircuit[circuit[i]['pin'][0]][circuit[i]
                      ['pin'][1]] = circuit[i]['voltage']
    trackPoint = circuit[i]['pin'][1]
    trackElement = i


(ADMatrix, pinList) = getAdMatrix(circuit)
print(ADMatrix)
basicMatrix = getBasicMatrix(ADMatrix, pinList)
print('bm', basicMatrix)
superBasicMatrix = findParallel(basicMatrix[0], basicMatrix[1], 0, [])
print(superBasicMatrix)
