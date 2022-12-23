import importlib
import os
import re

from rdflib import Graph
import pyswip

from ontology.ontology import Ontology
from plugins.hydra.hydra import Hydra
from plugins.nmap.nmap import Nmap
from plugins.outputParser import OutputParser


def find_plugins(exclude=[]):
    # find all plugins available and initialize them
    plugins = {}
    # print(f'Excluding plugins {exclude}')
    for f in os.listdir('plugins'):
        # print(f'current plugin {f}')
        if (f == '__pycache__' or '.py' in f or f in exclude):
            continue
        # print(f'starting plugin {f}')
        module = importlib.import_module("plugins.%s.%s" % (f, f))
        class_name = ''.join(map(str.capitalize, f.split('_')))
        class_ = getattr(module, class_name)()
        plugins[f] = class_

    return plugins

g = Graph()
g.parse('ontology/demo.ttl')
ontology = Ontology(g)


#
# hydra = Hydra()
# o = hydra.brute_hydra_ssh("192.168.0.106", 22)
#
# ontology.putOutputIntoOntology(o)

plugins = find_plugins([])
#
# ontology.putOutputIntoOntology(o)
prolog = pyswip.Prolog()

prolog.consult('ontology/tools.pl')
prolog.consult('ontology/parser.pl')
for query_result in prolog.query('tools(Tool, Command)'):
    print(query_result)
    if query_result['Tool'] in plugins:
        sc = getattr(plugins[query_result['Tool']], 'execute_command')
        command = [query_result['Command']]
        result = sc(*command)
        print(result)
        ontology.putOutputIntoOntology(result)

ontology.saveToFile('scan.ttl')