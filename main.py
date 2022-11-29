import rdflib
from rdflib import Graph, OWL, RDF, FOAF
from rdflib.extras.infixowl import Class
from rdflib.namespace import NamespaceManager, Namespace
from rdflib.plugins.sparql import prepareQuery

from ontology.ontology import Ontology
from plugins.hydra.hydra import Hydra
from plugins.nmap.nmap import Nmap

g = Graph()
g.parse('ontology/demo.ttl')

ontology = Ontology(g)



hydra = Hydra()
o = hydra.brute_hydra_ssh("192.168.0.106", 22)

print(o)

ontology.putOutputIntoOntology(o)

# gobuster = Gobuster(g)
# result = gobuster.enum_dir("192.168.0.106", 8000)

# g.serialize(destination="ontology/scan.ttl")
