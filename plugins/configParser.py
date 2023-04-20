import os
import json
import re

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
        properties.append(('profileName', name))
        for property in self.onto_classes['Profile']:
            if property in profile_config:
                properties.append((property, profile_config[property]))
        profile = self.convertToClass(('Profile', properties))

        for requirement in profile_config['Requirement']:
            value = profile_config['Requirement'][requirement]
            requirement_uri = self.add_requirement(requirement, value)
            self.graph.add((profile, self.links['Requirement'][0][1],requirement_uri))

        for parameter in profile_config['Parameter']:
            parameter_uri = self.add_parameter(parameter)
            self.graph.add((profile, self.links['Parameter'][0][1],parameter_uri))

        for result in profile_config['Result']:
            result_uri = self.add_result(result)
            self.graph.add((profile, self.links['Result'][0][1], result_uri))


        return profile

    def add_result(self, result):
        properties = []
        properties.append(('result',result))
        return self.convertToClass(('Result', properties))
    def add_requirement(self, requirement, value):
        properties = [('requirement', requirement), ('value', value)]
        return self.convertToClass(('Requirement', properties))

    def add_parameter(self, parameter):
        properties = [('parameter', parameter)]
        return self.convertToClass(('Parameter', properties))
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
            self.add_property_to_object(obj, property)
        return obj

    def createOntologyObject(self, name):
        ontoClass = URIRef(self.lookup['ontology'] + "#" + str(name))
        i = 1
        for s, p, o in self.graph.triples((None, None, ontoClass)):
            n = s.__str__().replace(o.__str__(), '')
            i = max(int(n) + 1, i)
        object = URIRef(self.lookup['ontology'] + "#" + str(name) + str(i))
        self.graph.add((object, RDF.type, self.lookup[name]))
        return object

    def add_property_to_object(self, object, property):
        propertyName = property[0]
        propertyValue = property[1]
        self.graph.add((object, self.lookup[propertyName], Literal(propertyValue)))

    def read_config_file(self, profile, prolog_output=None):
        for file_name in os.listdir('plugins/' + profile):
            if file_name == '__pycache__' or '.py' in file_name:
                continue
            file = open('plugins/' + profile + '/' + file_name)
            data = json.load(file)
            self.config_to_onto(data)
            prolog_str = self.config_to_prolog(data)

            if prolog_output is not None:
                f = open(prolog_output, 'a+')
                f.write(prolog_str)

    def config_to_prolog(self, config_json):
        tool = config_json['Tool']

        tool_predicates = ""
        profile_predicates = ""
        command_predicates = ""

        # tool(<tool_name>, <profile_name>)
        # profile(<profile_name>, <[parameters]>) :- requirement(value), ... ,  requirement(value).
        for profile in tool['Profile']:
            profile_config = tool['Profile'][profile]
            tool_predicates += f"tool({tool['toolName']}, {profile}).\n"

            requirements = self.configure_dict_string(profile_config['Requirement'], '(', ')')
            parameters = self.configure_dict_string(profile_config['Parameter'], '=','')
            command_predicates += self.configure_command(profile_config['Command'], profile)
            profile_predicates += f"profile({profile}, [{parameters}]) :- {requirements}, {profile}([{parameters}], Command), \+executed({profile}, Command).\n"

        return tool_predicates + "\n" + profile_predicates + "\n" + command_predicates

    def configure_dict_string(self, config_json, value_start, value_end):
        str = ""
        for key in config_json:
            if str != "":
                str += ', '
            value = config_json[key]
            value_str = ""
            if type(value) is list:
                for v in value:
                    if value_str != "":
                        value_str += ', '
                    value_str += v
            else:
                value_str = value

            str += f"{key}{value_start}{value_str}{value_end}"
        return str


    def configure_command(self, command, profile_name):
        command_predicate = f"{profile_name}(Parameters, Command) :- \n"
        parameters = re.findall(f'<([a-z0-9-]+)>', command)
        formated_command = re.sub(f'(<[a-z0-9-]+>)', '~w', command)
        parameters_str = ""
        for parameter in parameters:
            if parameters_str != "":
                parameters_str += ", "
            parameters_str += f"Parameters.{parameter}"

        return command_predicate + f"\tformat_command(\"{formated_command}\", [{parameters_str}], Command). \n\n"


    def read_profiles(self, prolog_output=None):
        if prolog_output is not None:
            # Clear file
            f = open(prolog_output, 'w')
            headers = ":- discontiguous tool/2.\n:- discontiguous profile/2.\n:- dynamic executed/2.\n:- dynamic connection/1.\n\n"
            f.write(headers)

        for f in os.listdir('plugins'):
            if (f == '__pycache__' or '.py' in f):
                continue
            self.read_config_file(f, prolog_output)


