import json
import sys

resistSum = 0

circuit = json.load(open(sys.argv[1]))
#print(circuit)

#calculate resistance
#temp = circuit["0"]
#print(temp)



def parallelResist (parallel):
#  print(parallel["value"])
  pList = parallel["value"]
  for i in range (0, len(pList)):
#    print(pList[i])
    for j in range (0, len(pList[i])):
#      print(type(pList))
      print(pList[i][str(j)])
    

parallelResist(circuit["1"])