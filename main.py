from rdflib import Graph
import plugins.nmap.nmap as nmp
import re
from plugins.gobuster.gobuster import Gobuster
from plugins.hydra.hydra import Hydra
from plugins.outputParser import OutputParser

g = Graph()
g.parse("ontology/demo.ttl")

hydra = Hydra(g)
#o = hydra.brute_hydra_ssh("192.168.0.106", 22)

f = open("temp.txt", "r")
hydraOutput = f.read()

f = open("test2.txt", "r")
gobusterOutput = f.read()

hydraParser = {'ipAddress': 'host: ',
        'protocol':'\]\[',
        'port':'^\[',
        'username':'login: ',
        'password':'password: '
               }
hydraLineStart = '\[\d+\]'

gobusterParser = {'page': '2K', 'status': 'Status: ' , 'size': 'Size: ' , 'redirect': '--> '}
gobusterLinestart = '\['

outputParser = OutputParser()
resultHy = outputParser.stringParse(gobusterOutput, gobusterParser, gobusterLinestart)
resultGo = outputParser.stringParse(hydraOutput, hydraParser, hydraLineStart)

for item in resultGo:
    for key in item:
        print(f'{key}: {item[key]}')
    print("-----------------")

for item in resultHy:
    for key in item:
        print(f'{key}: {item[key]}')
    print("-----------------")





gobuster = Gobuster(g)
#result = gobuster.enum_dir("192.168.0.106", 8000)


plugin = nmp.Nmap(g)
#plugin.enum_fast_scan("10.110.187.192")

g.serialize(destination="ontology/scan.ttl")


