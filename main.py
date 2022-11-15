from enum import Enum

from owlready import get_ontology, onto_path, Thing, Property
from rdflib import Graph, Namespace
from ontology_alchemy import Ontology, Session
import xml.etree.ElementTree as ET

from rdflib.namespace import NamespaceManager

import plugins.nmap.nmap as nmp
from ontology import ontology
from plugins.gobuster.gobuster import Gobuster
from plugins.hydra.hydra import Hydra



dev = ontology.Device()
ip = ontology.IpAddress()

dev.addresses.append(ip)

ip.Ipv4.append("192.168.0.106")

for address in dev.addresses:
    print(address.Ipv4)

ontology.save()

hydra = Hydra()
o = hydra.brute_hydra_ssh("192.168.0.106", 22)

print(o)

#gobuster = Gobuster(g)
#result = gobuster.enum_dir("192.168.0.106", 8000)

#plugin = nmp.Nmap(g)
#plugin.enum_fast_scan("10.110.187.192")

#g.serialize(destination="ontology/scan.ttl")


