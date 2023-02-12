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

ip = input("Give the target ip:\n")
r = [{}]

r[0]['ipv4'] = ip

ontology.putOutputIntoOntology(r)
ontology.saveToFile('ontology/test.ttl')

hasExecuted = True
execTools = []
plugins = find_plugins([])
while hasExecuted:
    prolog = pyswip.Prolog()

    prolog.consult('ontology/parser.pl')
    prolog.consult('ontology/tools.pl')

    hasExecuted = False
    for result in prolog.query('tools(Tool, Command)'):
        if result['Tool'] in plugins and result not in execTools:
            print(f"Executing tool {result['Tool']} with the command {result['Command']}")
            sc = getattr(plugins[result['Tool']], 'execute_command')
            command = [result['Command']]
            output = sc(*command, ip)
            print(output)
            ontology.putOutputIntoOntology(output)
            ontology.saveToFile('ontology/test.ttl')

            execTools.append(result)
            hasExecuted = True




ontology.saveToFile('ontology/test.ttl')