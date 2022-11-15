from rdflib import Graph
import plugins.nmap.nmap as nmp
from plugins.gobuster.gobuster import Gobuster
from plugins.hydra.hydra import Hydra

g = Graph()
g.parse("ontology/demo.ttl")

#hydra = Hydra(g)
#hydra.brute_hydra_ssh("10.110.47.255",22)

gobuster = Gobuster(g)
result = gobuster.enum_dir("10.110.187.192", 8000)
print(result)

plugin = nmp.Nmap(g)
plugin.enum_fast_scan("10.110.187.192")

g.serialize(destination="ontology/scan.ttl")


