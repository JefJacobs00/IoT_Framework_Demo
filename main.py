import json
import re

import rdflib
from rdflib import Graph, RDF, OWL

from plugins.gobuster.gobuster import Gobuster
from plugins.hydra.hydra import Hydra
from plugins.nmap.nmap import Nmap
from plugins.outputParser import OutputParser

g = Graph()
g.parse("ontology/demo.ttl")

hydra = Hydra()
o = hydra.brute_hydra_ssh("192.168.0.106", 22)

print(o)

#gobuster = Gobuster(g)
#result = gobuster.enum_dir("192.168.0.106", 8000)

plugin = Nmap()
result = plugin.enum_terminal("192.168.0.212")
print(result)

# f = open('test3.txt','r')
# f.write(result)

# result = f.read()

print(result)
test = {'port':{'start':'\n', 'end':'/'},
        'state':{'start':' ', 'end':' '},
        'service':{'start':' ', 'end':'$'},
        }

lines = re.findall('\n\d+/.*',result)
for line in lines:
    for key in test:
        print(re.findall(f'({test[key]["start"]})([a-zA-Z0-9.@/_-]+)({test[key]["end"]})',line))

print(lines)
#g.serialize(destination="ontology/scan.ttl")


