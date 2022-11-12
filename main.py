from rdflib import Graph
import plugins.nmap.nmap as nmp
from plugins.gobuster.gobuster import Gobuster

g = Graph()
g.parse("ontology/ontology.ttl")

gobuster = Gobuster(g)

result = gobuster.enum_dir("192.168.0.212", 8080)

print(result)

plugin = nmp.Nmap(g)
#plugin.enum_fast_scan("192.168.0.212")

g.serialize(destination="ontology/scan.ttl")


