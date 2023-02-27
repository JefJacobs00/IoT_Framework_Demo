import importlib
import os
import re
from threading import Thread

from rdflib import Graph
import pyswip
from ontology.ontology import Ontology
from plugins.configParser import ConfigParser


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
    ontology.putOutputIntoOntology(output)
    ontology.saveToFile('ontology/knowledgebase.ttl')
    print(output)
    running_scan -= 1


running_scan = 0
def start_scanning(target):
    ontology.putOutputIntoOntology(target)
    ontology.saveToFile('ontology/knowledgebase.ttl')

    has_executed = True

    executed_tools = []

    prolog = pyswip.Prolog()
    prolog.consult('ontology/tools.pl')
    prolog.consult('ontology/parser.pl')
    while has_executed or (running_scan > 0):
        prolog.query('load_ontology()')

        has_executed = False
        for result in prolog.query('tools(Tool, Command)'):
            if result['Tool'] in plugins and result not in executed_tools:
                thread = Thread(target=execute_scan, args=(result['Tool'], result['Command'], ip))
                thread.start()
                executed_tools.append(result)
                has_executed = True

    ontology.saveToFile('ontology/knowledgebase.ttl')


g = Graph()
g.parse('ontology/knowledge_ontology.ttl')
ontology = Ontology(g)

plugins = find_plugins([])
# ip = input("Give the target ip:\n")
ip = "192.168.0.106"
r = [{}]

# r[0]['ipv4'] = ip
# ontology.putOutputIntoOntology(r)
# ontology.saveToFile('ontology/knowledgebase.ttl')

c = ConfigParser()
c.read_profiles('ontology/tools_config.pl')


# prolog = pyswip.Prolog()
#
# prolog.consult('ontology/tools2.pl')
# prolog.consult('ontology/parser.pl')
#
# prolog.query('load_ontology()')
# profiles = {}
# for profile in prolog.query('profile(Profile)'):
#     profiles[profile['Profile']] = {'Requirements': [], 'Values': []}
#
# for profile in profiles:
#     for requirement in prolog.query(f'profile_requirement({profile}, Requirement)'):
#         profiles[profile]['Requirements'].append(requirement['Requirement'])
#     for value in prolog.query(f'profile_value({profile}, Value)'):
#         profiles[profile]['Values'].append(value['Value'])
#
# for profile in profiles:
#     requirements = str(profiles[profile]["Requirements"]).replace("\'", "")
#     values = str(profiles[profile]["Values"]).replace("\'", "")
#     print(profile)
#     for results in prolog.query(f'profile_requirements({profile}, {requirements}, {values})'):
#         print(results)

