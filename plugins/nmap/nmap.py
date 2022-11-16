import json

import nmap
import common.utils as utils
import ontology.ontology_wrapper as ontology


class Nmap:
    def __init__(self, ontology):
        self.ontology = ontology

    def enum_fast_scan(self, host):
        scanner = nmap.PortScanner()
        flags = ['-F']
        sc = scanner.scan(host, arguments=' '.join(flags))
        result = scanner._scan_result['scan']

        return result
