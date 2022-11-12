import nmap
import common.utils as utils
import ontology.ontology_wrapper as ontology


class Nmap:
    def __init__(self, ontology):
        self.ontology = ontology

    def enum_fast_scan(self, host):
        scanner = nmap.PortScanner()
        flags = ['-P']
        sc = scanner.scan(host, arguments=' '.join(flags))
        result = scanner._scan_result['scan']

        unwanted_keys = ['addresses', 'status', 'reason', 'conf', 'extrainfo']
        result = utils.rm_fields(result, unwanted_keys)
        self.save_output(result)

    def save_output(self, result):
        onto = ontology.ontology_wrapper()
        for ip in result:
            dev = onto.add_device_to_onto(ip, self.ontology)
            for protocol in result[ip]:
                for port in result[ip][protocol]:
                    service = result[ip][protocol][port]['name']
                    state = result[ip][protocol][port]['state']
                    onto.add_port_to_onto(port, service, state, dev, self.ontology)
