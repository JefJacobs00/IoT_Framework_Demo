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


def execute_scan(tool, profile,  command, parameters_uri, parameters, target):
    global running_scan
    sc = getattr(plugins[tool], 'execute_command')
    output = sc(command, target, parameters_uri, parameters, profile)
    # TODO add parameters
    ontology.putOutputIntoOntology(output, parameters)
    ontology.saveToFile('ontology/knowledgebase.ttl')
    #print(output)


def get_next_profile(prolog):
    profile = {}
    for result in prolog.query(f'tools_score(Tool, Profile, Command, Parameter)'):
        profile['Tool'] = result['Tool']
        profile['Command'] = result['Command']
        profile['name'] = result['Profile']
        uri_parameters = []
        parameters = {}
        for parameter in result['Parameter']:
            if 'uri' in parameter:
                match = re.search(r'=\((.*?),\s*(?P<Uri>.*?)\)', parameter)
                uri_parameters.append(match['Uri'])
            else:
                match = re.search(r'=\((?P<Key>.*?),\s*(?P<Value>.*?)\)', parameter)
                parameters[match['Key']] = match['Value']
        profile['uri_parameters'] = uri_parameters
        profile['parameters'] = parameters
        break

    return profile

def start_scanning(target):
    has_executed = True

    prolog = pyswip.Prolog()
    prolog.consult('ontology/tools.pl')
    while has_executed:
        has_executed = False
        for result in prolog.query("load_ontology(\"ontology/knowledgebase.ttl\")"):
            pass
        time.sleep(0.2)
        profile = get_next_profile(prolog)
        if len(profile) > 0:
            execute_scan(profile['Tool'], profile['name'], profile['Command'], profile['uri_parameters'], profile['parameters'], target)
            has_executed = True

    ontology.saveToFile('ontology/knowledgebase.ttl')





g = Graph()

g.parse('ontology/tools_ontology.ttl')
g.parse('ontology/knowledge_ontology.ttl')

ontology = Ontology(g, 'ontology/knowledgebase.ttl')

plugins = find_plugins(['tool.py'])
# ip = input("Give the target ip:\n")
ip = "192.168.0.102"
r = [{'ipv4':ip, 'firmwarePath':'~/Downloads/studentv2'}]

ontology.putOutputIntoOntology(r)
ontology.saveToFile('ontology/knowledgebase.ttl')

c = ConfigParser()
c.read_profiles('ontology/tools_config.pl')

start_time = time.time()
start_scanning(r[0]["ipv4"])
end = time.time()

print("Scanning took: " + str(end - start_time))


