import os
import json

from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


class ConfigParser:
    def __int__(self):
        self.graph = Graph()
        self.graph.parse('ontology/tools_ontology.ttl')

        self.__queryClasses = prepareQuery("SELECT ?s WHERE { ?s rdf:type owl:Class }", )
        self.__queryDataProperties = prepareQuery("SELECT ?s ?o ?d WHERE { ?s rdf:type owl:DatatypeProperty; "
                                                  "rdfs:domain ?class}", )
        self.__queryObjectProperty = prepareQuery(
            "SELECT ?s ?range ?domain WHERE { ?s rdf:type owl:ObjectProperty; rdfs:domain "
            "?domain; rdfs:range ?range .}", )

        self.onto_classes = self.__get_classes()
        print(self.onto_classes)

    def __get_classes(self):
        ontology_classes = {}
        for row in self.graph.query(self.__queryClasses):
            key = row.s.__str__().split('#')[1]
            ontology_classes[key] = []
            for dp in self.graph.query(self.__queryDataProperties, initBindings={'class': row.s}):
                value = dp.s.__str__().split('#')[1]
                ontology_classes[key].append(value)
        return ontology_classes

    def config_to_onto(self, config_json):
        print(self.onto_classes)

    def read_config_file(self, plugin):
        for file_name in os.listdir('plugins/' + plugin):
            if (file_name == '__pycache__' or '.py' in file_name):
                continue
            file = open('plugins/' + plugin + '/' + file_name)
            self.config_to_onto(json.load(file))

    def read_plugins(self):
        for f in os.listdir('plugins'):
            if (f == '__pycache__' or '.py' in f):
                continue
            self.read_config_file(f)

# Lees de config files van de tools in en maak aan de hand van deze config files de ontology data aan (tools_ontology.ttl)
# save deze dan in een tools.ttl bestand die alle tools en nodige data bevatten.
# insperatie van ontology.py
