from rdflib import Graph
import plugins.nmap.nmap as nmp
import re
from plugins.gobuster.gobuster import Gobuster
from plugins.hydra.hydra import Hydra
from plugins.outputParser import OutputParser

g = Graph()
g.parse("ontology/demo.ttl")

hydra = Hydra(g)
o = hydra.brute_hydra_ssh("192.168.0.106", 22)
print(o)

gobuster = Gobuster(g)
result = gobuster.enum_dir("192.168.0.106", 8000)
print(result)

plugin = nmp.Nmap(g)
#plugin.enum_fast_scan("10.110.187.192")

g.serialize(destination="ontology/scan.ttl")


