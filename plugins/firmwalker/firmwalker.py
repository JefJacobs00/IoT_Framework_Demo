import re

from plugins.tool import Tool


class Firmwalker(Tool):
    def __init__(self, ontology):
        parser = {'accountUsername': '\[Account\]:', 'hashValue': '\[Hash.*\]:', 'hashFunction': '\[Hash '}
        line_start = ''
        super().__init__(ontology=ontology, parser=parser, info_start='\[')

    def execute_command(self, command, target, parameters_uri, parameters, profile):
        return super().execute_command(command, target, parameters_uri, parameters, profile)