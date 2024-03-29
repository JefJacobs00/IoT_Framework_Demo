import re

from plugins.tool import Tool


class Nmap(Tool):
    def __init__(self, ontology):
        parser = re.compile(r'(?P<portNumber>[0-9]+)/(?P<protocol>[a-z]+)(\s+)(?P<portStatus>[a-z]+)(\s+)(?P<serviceName>[a-z?/]*)')
        super().__init__(ontology=ontology, parser=parser,info_end='\n')

    def execute_command(self, command, target, parameters_uri, parameters, profile):
        return super().execute_command(command, target, parameters_uri, parameters, profile)
