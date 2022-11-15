from owlready import get_ontology, Thing, Property, ANNOTATIONS

onto = get_ontology("http://test.org/demo.owl")

# Class

class Device(Thing):
    ontology = onto


class IpAddress(Thing):
    ontology = onto


class Port(Thing):
    ontology = onto


class Account(Thing):
    ontology = onto

# object property


class device_has_address(Property):
    ontology = onto
    domain = [Device]
    range = [IpAddress]

# Data property


class Ipv4(Property):
    ontology = onto
    domain = [IpAddress]
    range = [str]

def save():
    onto.save("test.owl")


ANNOTATIONS[device_has_address]["python_name"] = "addresses"