import os
import json

from rdflib import Graph, RDF
from rdflib.plugins.sparql import prepareQuery


class ConfigParser:
    def __init__(self):
        self.graph = Graph()
        self.graph.parse('ontology/tools_ontology.ttl')

        self.__queryClasses = prepareQuery("SELECT ?s WHERE { ?s rdf:type owl:Class }", )
        self.__queryDataProperties = prepareQuery("SELECT ?s ?o ?d WHERE { ?s rdf:type owl:DatatypeProperty; "
                                                  "rdfs:domain ?class}", )
        self.__queryObjectProperty = prepareQuery(
            "SELECT ?s ?range ?domain WHERE { ?s rdf:type owl:ObjectProperty; rdfs:domain "
            "?domain; rdfs:range ?range .}", )

        self.lookup = self.__createLookup()
        self.onto_classes = self.__get_classes()
        self.links = self.__getLinks()

    def __createLookup(self):
        lookup = {}
        for s, p, o in self.graph.triples((None, RDF.type, None)):
            if (s.__str__().__contains__("#")):
                key = s.__str__().split('#')[1]
                lookup[key] = s
            else:
                lookup['ontology'] = s.__str__()
        return lookup
    def __getLinks(self):
        links = {}
        for c in self.onto_classes.keys():
            links[c] = []
            for op in self.graph.query(self.__queryObjectProperty, initBindings={'range': self.lookup[c]}):
                key = op.domain.__str__().split('#')[1]
                links[c].append((key, op.s))
        return links
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
        for key in config_json:
            self.recursive_search(config_json[key],key,)

    def find_properties(self, class_name, config_json):
        properties = self.create_properties(class_name)
        self.recursive_search(config_json, class_name, properties)
        return (class_name, properties)

    def create_properties(self, class_name):
        properties = {}
        for key in self.onto_classes[class_name]:
            properties[key] = ""

        return properties
    def recursive_search(self, config_json, class_name):
        for key in config_json:
            if type(config_json[key]) is dict:
                self.recursive_search(config_json[key], key)

    def read_config_file(self, plugin):
        for file_name in os.listdir('plugins/' + plugin):
            if file_name == '__pycache__' or '.py' in file_name:
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
