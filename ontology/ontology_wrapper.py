from rdflib import Graph, Namespace, URIRef, RDF, Literal



class ontology_wrapper:
    uri = "http://www.semanticweb.org/jef/ontologies/2022/10/onto"
    namespace = Namespace(uri + "#")

    def add_device_to_onto(self, ip, onto):
        dev = URIRef(self.uri + "#dev" + ip)
        onto.add((dev, RDF.type, self.namespace.Device))
        ip1 = URIRef(self.uri + "#address" + ip)
        onto.add((ip1, RDF.type, self.namespace.IpAddress))
        onto.add((ip1, self.namespace.addressValue, Literal(ip)))
        onto.add((dev, self.namespace.deviceAddress, ip1))
        return dev

    def add_port_to_onto(self, portNumber, portStatus, portService, dev, onto):
        port = URIRef(self.uri + "#port" + str(portNumber))
        onto.add((port, RDF.type, self.namespace.Port))
        onto.add((port, self.namespace.portNumber, Literal(portNumber)))
        onto.add((port, self.namespace.portService, Literal(portService)))
        onto.add((port, self.namespace.portStatus, Literal(portStatus)))
        onto.add((dev, self.namespace.devicePort, port))