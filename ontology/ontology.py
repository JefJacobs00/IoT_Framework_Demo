from rdflib import Graph, RDF, URIRef, Literal
from rdflib.plugins.sparql import prepareQuery


class Ontology:
    def __init__(self, graph: Graph, existing_info=None):
        self.graph = graph
        self.__queryClasses = prepareQuery("SELECT ?s WHERE { ?s rdf:type owl:Class }", )
        self.__queryDataProperties = prepareQuery("SELECT ?s ?o ?d WHERE { ?s rdf:type owl:DatatypeProperty; "
                                                  "rdfs:domain ?class}", )
        self.__queryObjectProperty = prepareQuery(
            "SELECT ?s ?range ?domain WHERE { ?s rdf:type owl:ObjectProperty; rdfs:domain "
            "?domain; rdfs:range ?range .}", )

        self.lookup = self.__createLookup()
        self.ontology_classes = self.__getClasses()
        self.links = self.__getLinks()
        self.graph = Graph()
        if existing_info is not None:
            self.graph.parse(existing_info)
            self.graph.parse('./ontology/tools.ttl')

    def __createLookup(self):
        lookup = {}
        for s, p, o in self.graph.triples((None, RDF.type, None)):
            if (s.__str__().__contains__("#")):
                key = s.__str__().split('#')[1]
                lookup[key] = s
            else:
                lookup['ontology'] = s.__str__()
        return lookup

    def __getClasses(self):
        ontology_classes = {}
        for row in self.graph.query(self.__queryClasses):
            key = row.s.__str__().split('#')[1]
            ontology_classes[key] = []
            for dp in self.graph.query(self.__queryDataProperties, initBindings={'class': row.s}):
                value = dp.s.__str__().split('#')[1]
                ontology_classes[key].append(value)
        return ontology_classes

    def __getLinks(self):
        links = {}
        for c in self.ontology_classes.keys():
            links[c] = []
            for op in self.graph.query(self.__queryObjectProperty, initBindings={'range': self.lookup[c]}):
                key = op.domain.__str__().split('#')[1]
                links[c].append((key, op.s))
        return links

    def findClassFromProperty(self, property: str):
        for key in self.ontology_classes:
            if self.ontology_classes[key].__contains__(property):
                return key

    def putOutputIntoOntology(self, output: list):
        structured = []
        for line in output:
            structured.append(self.structureInfo(line))
        if 'Profile' in structured:
            print('Calculate score for: '+{structured['Profile']})
        for line in structured:
            objects = []
            for key in line:
                objects.append((key, self.convertToClass((key, line[key]))))
            for key, object in objects:
                for link in self.links[key]:
                    test = [key for key in objects if key[0] == link[0]]
                    if len(test) > 0:
                        self.graph.add((test[0][1], link[1], object))

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

    def addPropertyToObject(self, object, property):
        propertyName = property[0]
        propertyValue = property[1]
        self.graph.add((object, self.lookup[propertyName], Literal(propertyValue)))

    def createOntologyObject(self, name):
        ontoClass = URIRef(self.lookup['ontology'] + "#" + str(name))
        i = 1
        for s, p, o in self.graph.triples((None, None, ontoClass)):
            i = int(s.__str__()[-1:]) + 1
        object = URIRef(self.lookup['ontology'] + "#" + str(name) + str(i))
        self.graph.add((object, RDF.type, self.lookup[name]))
        return object

    def structureInfo(self, info: dict):
        information = {}
        for property in info:
            key = self.findClassFromProperty(property)
            if key is not None:
                if not information.keys().__contains__(key):
                    information[key] = []
                information[key].append((property, info[property]))

        return information

    def saveToFile(self, path: str):
        self.graph.serialize(destination=path)
