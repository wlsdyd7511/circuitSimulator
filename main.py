import json
import sys
import copy

trackPoint = str()
trackElement = str()

def find(pin, tracking):
  temp = list()
  for i in circuit:
    if(pin in circuit[i]['pin']):
      if  i != tracking:
        temp.append(i)
  return temp

with open(sys.argv[1], 'r') as f:
  circuit = json.load(f)
#print(circuit)
editCircuit = copy.deepcopy(circuit)
#circuitOut = json.dumps(circuit, indent = 4)
#print(circuitOut)
#print(type(circuitOut))

for i in circuit:
  #print(circuit[i])
  if(circuit[i]['type'] == 'DCPower'):
    editCircuit[circuit[i]['pin'][0]] = dict()
    editCircuit[circuit[i]['pin'][0]][circuit[i]['pin'][1]] = circuit[i]['voltage']
    trackPoint = circuit[i]['pin'][1]
    trackElement = i
    linked = find(trackPoint, trackElement)
    print(linked)




print(editCircuit)