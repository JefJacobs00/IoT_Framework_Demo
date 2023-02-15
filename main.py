import importlib
import os
import re
from threading import Thread

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

def execute_scan(tool, command, target):
    global running_scan
    running_scan += 1
    print(f"Executing tool {tool} with the command {command}")
    sc = getattr(plugins[tool], 'execute_command')
    output = sc(command, target)
    print(output)
    ontology.putOutputIntoOntology(output)
    ontology.saveToFile('ontology/test.ttl')
    running_scan -= 1

g = Graph()
g.parse('ontology/demo.ttl')
ontology = Ontology(g)

#ip = input("Give the target ip:\n")
ip = "192.168.0.106"
r = [{}]

r[0]['ipv4'] = ip

ontology.putOutputIntoOntology(r)
ontology.saveToFile('ontology/test.ttl')

has_executed = True
running_scan = 0

execTools = []
plugins = find_plugins([])

prolog = pyswip.Prolog()
prolog.consult('ontology/tools.pl')
while has_executed or (running_scan > 0):
    prolog.consult('ontology/parser.pl')

    has_executed = False
    for result in prolog.query('tools(Tool, Command)'):
        if result['Tool'] in plugins and result not in execTools:
            thread = Thread(target=execute_scan, args=(result['Tool'], result['Command'], ip))
            thread.start()
            execTools.append(result)
            has_executed = True




ontology.saveToFile('ontology/test.ttl')