import json
from subprocess import Popen, PIPE

import nmap
import common.utils as utils
import ontology.ontology_wrapper as ontology
from plugins.outputParser import OutputParser


class Nmap:
    def __init__(self):
        self.parser = ""
    def enum_terminal(self, host):
        cmd = f'nmap -F {host}'
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
        (output, err) = p.communicate()
        print(err)


        output = output.decode("utf-8")
        return output
    def enum_fast_scan(self, host):
        scanner = nmap.PortScanner()
        flags = ['-F']
        sc = scanner.scan(host, arguments=' '.join(flags))
        result = scanner._scan_result['scan']
        return result
