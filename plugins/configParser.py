import os
import json

from rdflib import Graph, RDF, URIRef, Literal
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
        self.graph = Graph()

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
        self.add_tool(config_json)
        self.add_profiles(config_json)
        self.graph.serialize(destination='ontology/tools.ttl')


    def add_tool(self, config_json):
        tools = self.recursive_search(config_json, 'Tool')
        properties = []
        for property in self.onto_classes['Tool']:
            properties.append((property, tools[property]))
        return self.convertToClass(('Tool', properties))

    def add_profiles(self, config_json):
        profiles_json = self.recursive_search(config_json, 'Profile')
        for profile in profiles_json:
            self.add_profile(profile, profiles_json[profile])
        print(profiles_json)
    def add_profile(self, name, profile_config):
        properties = []
        properties.append(('name', name))
        for property in self.onto_classes['Profile']:
            if property in profile_config:
                properties.append((property, profile_config[property]))
        profile = self.convertToClass(('Profile', properties))

        for requirement in profile_config['Requirement']:
            requirement_uri = self.add_requirement(requirement)
            self.graph.add((profile, self.links['Requirement'][0][1],requirement_uri))

        for result in profile_config['Result']:
            result_uri = self.add_result(result)
            self.graph.add((profile, self.links['Result'][0][1], result_uri))


        return profile

    def add_result(self, result):
        properties = []
        properties.append(('result',result))
        return self.convertToClass(('Result', properties))
    def add_requirement(self, requirement):
        properties = []
        properties.append(('requirement',requirement))
        return self.convertToClass(('Requirement', properties))
    def recursive_search(self, config, search_key):
        for key in config:
            if key == search_key:
                return config[key]
            elif type(config[key]) is dict:
                return self.recursive_search(config[key], search_key)

    def checkIfExists(self, type, properties):
        for s, p, o in self.graph.triples((None, None, self.lookup[type])):
            equal = True
            obj = None
            for prop in properties:
                for s, p, o in self.graph.triples((s, self.lookup[prop[0]], None)):
                    if o.__str__() == prop[1]:
                        equal = True and equal
                        obj = s
                    else:
                        equal = False
            if equal:
                return obj

    def convertToClass(self, value: tuple):
        item = value[0]
        properties = value[1]
        obj = self.checkIfExists(item, properties)
        if obj is None:
            obj = self.createOntologyObject(item)

        for property in properties:
            self.addPropertyToObject(obj, property)
        return obj

    def createOntologyObject(self, name):

        ontoClass = URIRef(self.lookup['ontology'] + "#" + str(name))
        i = 1
        for s, p, o in self.graph.triples((None, None, ontoClass)):
            i = int(s.__str__()[-1:]) + 1
        object = URIRef(self.lookup['ontology'] + "#" + str(name) + str(i))
        self.graph.add((object, RDF.type, self.lookup[name]))
        return object

    def addPropertyToObject(self, object, property):
        propertyName = property[0]
        propertyValue = property[1]
        self.graph.add((object, self.lookup[propertyName], Literal(propertyValue)))

    def read_config_file(self, profile):
        for file_name in os.listdir('plugins/' + profile):
            if file_name == '__pycache__' or '.py' in file_name:
                continue
            file = open('plugins/' + profile + '/' + file_name)
            self.config_to_onto(json.load(file))

    def read_profiles(self):
        for f in os.listdir('plugins'):
            if (f == '__pycache__' or '.py' in f):
                continue
            self.read_config_file(f)

# Lees de config files van de tools in en maak aan de hand van deze config files de ontology data aan (tools_ontology.ttl)
# save deze dan in een tools.ttl bestand die alle tools en nodige data bevatten.
# insperatie van ontology.py
