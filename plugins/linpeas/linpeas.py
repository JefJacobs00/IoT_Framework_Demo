import re

from plugins.tool import Tool


class Linpeas(Tool):
    def __init__(self, ontology):
        parser = re.compile(r'')
        super().__init__(ontology=ontology,parser=parser,info_end='\n')

    def execute_command(self, command, target, parameters_uri, parameters, profile):
        return super().execute_command(command, target, parameters_uri, parameters, profile)