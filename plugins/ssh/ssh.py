import re

from plugins.tool import Tool


class Ssh(Tool):
    def __init__(self, ontology):
        parser = re.compile(r'')
        super().__init__(ontology=ontology, parser=parser,info_end='\n')

    def execute_command(self, command, target, parameters_uri, parameters, profile):
        print("Trying to get ssh connection: " + command.decode('utf8'))
        return {}