import importlib
import os
import re
import time
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
        class_ = getattr(module, class_name)(ontology)
        plugins[f] = class_

    return plugins


def execute_scan(tool, profile,  command, parameters, target):
    global running_scan
    print(f"Executing tool {tool} with the command {command}")
    sc = getattr(plugins[tool], 'execute_command')
    output = sc(command, target, parameters, profile)
    ontology.putOutputIntoOntology(output)
    ontology.saveToFile('ontology/knowledgebase.ttl')
    #print(output)


def get_next_profile(prolog):
    profile = {}
    for result in prolog.query(f'tools_score(Tool, Profile, Command, Parameter)'):
        profile['Tool'] = result['Tool']
        profile['Command'] = result['Command']
        profile['name'] = result['Profile']
        parameters = []
        for parameter in result['Parameter']:
            if 'uri' in parameter:
                test = re.search(r'=\((.*?),\s*(?P<Uri>.*?)\)', parameter)
                parameters.append(test['Uri'])
        profile['parameters'] = parameters
        break

    return profile

def start_scanning(target):
    has_executed = True

    prolog = pyswip.Prolog()
    prolog.consult('ontology/tools.pl')
    while has_executed:
        has_executed = False
        prolog.query("rdf_load('knowledgebase.ttl', [format('turtle')]).")
        time.sleep(0.2)
        profile = get_next_profile(prolog)
        if len(profile) > 0:
            execute_scan(profile['Tool'], profile['name'], profile['Command'], profile['parameters'], target)
            has_executed = True

    ontology.saveToFile('ontology/knowledgebase.ttl')





g = Graph()

g.parse('ontology/tools_ontology.ttl')
g.parse('ontology/knowledge_ontology.ttl')

ontology = Ontology(g, 'ontology/knowledgebase.ttl')

plugins = find_plugins(['tool.py'])
# ip = input("Give the target ip:\n")
ip = "192.168.0.102"
r = [{'ipv4':ip, 'firmwarePath':'~/Downloads/studentv1/'}]

ontology.putOutputIntoOntology(r)
ontology.saveToFile('ontology/knowledgebase.ttl')

c = ConfigParser()
c.read_profiles('ontology/tools_config.pl')

start_scanning(r[0]["ipv4"])



