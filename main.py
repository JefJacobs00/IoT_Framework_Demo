import re

from rdflib import Graph

from ontology.ontology import Ontology
from plugins.hydra.hydra import Hydra
from plugins.nmap.nmap import Nmap
from plugins.outputParser import OutputParser

g = Graph()
g.parse('ontology/demo.ttl')

ontology = Ontology(g)

nmap = Nmap()
output = nmap.enum_terminal("192.168.0.106")
outputParser = OutputParser()

m = re.compile(r'(?P<portNumber>[0-9]+)/(?P<protocol>[a-z]+)(\s+)(?P<portStatus>[a-z]+)(\s+)(?P<serviceName>[a-z?/]*)')
result = outputParser.stringParseMatcher(m, '\n', output)
for r in result:
    r['ipv4'] = "192.168.0.106"

print(result)
ontology.putOutputIntoOntology(result)

hydra = Hydra()
o = hydra.brute_hydra_ssh("192.168.0.106", 22)

ontology.putOutputIntoOntology(o)
#
# ontology.putOutputIntoOntology(o)


ontology.saveToFile('scan.ttl')