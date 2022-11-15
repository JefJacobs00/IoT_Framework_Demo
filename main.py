import rdflib
from rdflib import Graph, RDF, OWL

from plugins.hydra.hydra import Hydra

g = Graph()
g.parse("ontology/demo.ttl")

for s, p, o in g.triples((None, None, OWL.DatatypeProperty)):
    print(s)

hydra = Hydra()
o = hydra.brute_hydra_ssh("192.168.0.106", 22)


#gobuster = Gobuster(g)
#result = gobuster.enum_dir("192.168.0.106", 8000)

#plugin = nmp.Nmap(g)
#plugin.enum_fast_scan("10.110.187.192")

#g.serialize(destination="ontology/scan.ttl")


