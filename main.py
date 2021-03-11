import json
import sys

circuitl = list()

with open(sys.argv[1], 'r') as f:
  circuit = json.load(f)
#print(circuit)

for i in range(0, len(circuit)):
  circuitl.append(circuit[str(i)])
  print(circuitl)
