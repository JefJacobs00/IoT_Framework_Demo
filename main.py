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


def execute_scan(tool, profile,  command, target):
    global running_scan
    print(f"Executing tool {tool} with the command {command}")
    sc = getattr(plugins[tool], 'execute_command')
    output = sc(command, target, profile)
    ontology.putOutputIntoOntology(output)
    ontology.saveToFile('ontology/knowledgebase.ttl')
    print(output)


def get_runnable_profiles(prolog, executed_tools):
    profiles = {}
    for result in prolog.query(f'tools(Tool, Profile, Command)'):
        if result['Tool'] in plugins and result not in executed_tools:
            profile = result['Profile']
            properties = {}
            properties['Tool'] = result['Tool']
            properties['Command'] = result['Command']
            profiles[profile] = properties

    return profiles


def get_avg_profile_duration(prolog, profile):
    durations = []
    for times in prolog.query(f'profileDuration({profile}, Duration)'):
        durations.append(float(times['Duration']))

    if len(durations) == 0:
        return 0

    return sum(durations)/len(durations)

def get_avg_profile_score(prolog, profile):
    score = []
    for times in prolog.query(f'profileScore({profile}, Score)'):
        score.append(int(times['Score']))

    if len(score) == 0:
        return 0

    return sum(score)/len(score)

def start_scanning(target):
    has_executed = True

    executed_tools = []

    prolog = pyswip.Prolog()
    prolog.consult('ontology/tools.pl')
    prolog.consult('ontology/parser.pl')
    prolog.consult('ontology/tools_config.pl')
    while has_executed:
        prolog.query('load_ontology()')
        has_executed = False
        profiles = get_runnable_profiles(prolog, executed_tools)
        for profile in profiles:
            profiles[profile]['avg_duration'] = get_avg_profile_duration(prolog, profile)
            profiles[profile]['avg_score'] = get_avg_profile_score(prolog, profile)

        sorted_keys = sorted(profiles, key=lambda x: profiles[x]['avg_duration'])
        print(profiles)

        for profile in sorted_keys:
            if profile not in executed_tools:
                executed_tools.append(profile)
                profile_properties = profiles[profile]
                execute_scan(profile_properties['Tool'], profile, profile_properties['Command'], target)
                has_executed = True
            else:
                print('HMM')

    ontology.saveToFile('ontology/knowledgebase.ttl')





g = Graph()

g.parse('ontology/tools_ontology.ttl')
g.parse('ontology/knowledge_ontology.ttl')

ontology = Ontology(g, 'ontology/knowledgebase.ttl')

plugins = find_plugins(['tool.py'])
# ip = input("Give the target ip:\n")
ip = "192.168.0.185"
r = [{'ipv4':ip}]

ontology.putOutputIntoOntology(r)
ontology.saveToFile('ontology/knowledgebase.ttl')

c = ConfigParser()
#c.read_profiles('ontology/tools_config.pl')

start_scanning(r[0]["ipv4"])



