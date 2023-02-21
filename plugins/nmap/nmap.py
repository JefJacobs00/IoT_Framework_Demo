import json
import re
from subprocess import Popen, PIPE

import nmap
from plugins.outputParser import OutputParser



class Nmap:
    def __init__(self):
        self.parser = re.compile(r'(?P<portNumber>[0-9]+)/(?P<protocol>[a-z]+)(\s+)(?P<portStatus>[a-z]+)(\s+)(?P<serviceName>[a-z?/]*)')

    def execute_command(self, command, target):
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
        (output, err) = p.communicate()
        outputParser = OutputParser()
        result = outputParser.stringParseMatcher(self.parser, '\n', output.decode("utf-8"))
        for r in result:
            r['ipv4'] = target
        return result
