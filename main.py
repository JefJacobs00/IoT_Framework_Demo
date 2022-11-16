import json
import re

import rdflib
from rdflib import Graph, RDF, OWL

from plugins.hydra.hydra import Hydra
from plugins.nmap.nmap import Nmap
from plugins.outputParser import OutputParser

g = Graph()
g.parse("ontology/demo.ttl")

#hydra = Hydra()
#o = hydra.brute_hydra_ssh("192.168.0.106", 22)


#gobuster = Gobuster(g)
#result = gobuster.enum_dir("192.168.0.106", 8000)

plugin = Nmap(g)
result = plugin.enum_fast_scan("192.168.0.212")


def rec(result):
    for i in result:
        print(result[i])

rec(result)
print(result)
#g.serialize(destination="ontology/scan.ttl")


