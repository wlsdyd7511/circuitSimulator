import json
import sys
import copy

trackPoint = str()
trackElement = str()


def getAdMatrix(cir):
  pinList = list()
  for k in cir:
    for pin in cir[k]["pin"]:
      if not pin in pinList:
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

  bMatrix = copy.deepcopy(matrix)
  pinToDel = list()
  for i in range(numPin):
    cntPin = 0
    for j in range(numPin):
      cntPin += matrix[i][j]
    if cntPin == 2:
      pinToDel.append(i)
  pinToDel.reverse()
  cntSeq = 0
  for i in pinToDel:
    del bMatrix[i]
    cntSeq += 1
    for j in range(numPin - cntSeq):
      del bMatrix[j][i]
  # print(bMatrix)
  return((matrix, bMatrix))


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


(adMatrix, sMatrix) = getAdMatrix(circuit)
print(adMatrix, '\n', sMatrix)
