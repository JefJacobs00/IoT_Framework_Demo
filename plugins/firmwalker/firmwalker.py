import re

from plugins.tool import Tool


class Firmwalker(Tool):
    def __init__(self, ontology):
        parser = re.compile(r'')
        super().__init__(ontology=ontology, parser=parser,info_end='\n')

    def execute_command(self, command, target, profile):
        return super().execute_command(command, target, profile)