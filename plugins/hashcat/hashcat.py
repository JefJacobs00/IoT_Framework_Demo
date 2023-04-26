import re

from plugins.tool import Tool


class Hashcat(Tool):
    def __init__(self, ontology):
        parser = {'passwordCleartext': ':'}
        line_start = ''
        super().__init__(ontology=ontology, parser=parser,info_end='\n')

    def execute_command(self, command, target, parameters, profile):
        return super().execute_command(command, target, parameters, profile)