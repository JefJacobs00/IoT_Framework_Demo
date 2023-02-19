import json
import re
from subprocess import Popen, PIPE

import nmap
from plugins.outputParser import OutputParser



class Nmap:
    def __init__(self):
        self.parser = re.compile(r'(?P<portNumber>[0-9]+)/(?P<protocol>[a-z]+)(\s+)(?P<portStatus>[a-z]+)(\s+)(?P<serviceName>[a-z?/]*)')
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

    def execute_command(self, command, target):
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
        (output, err) = p.communicate()
        outputParser = OutputParser()
        result = outputParser.stringParseMatcher(self.parser, '\n', output.decode("utf-8"))
        for r in result:
            r['ipv4'] = target
        return result
