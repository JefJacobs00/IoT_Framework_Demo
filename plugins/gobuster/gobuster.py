from plugins.tool import Tool

class Gobuster(Tool):
    def __init__(self, ontology):
        parser = {'page': '2K', 'status': 'Status: ', 'size': 'Size: ', 'redirect': '--> '}
        line_start = '\['
        super().__init__(ontology=ontology, parser=parser, info_start=line_start)

    def execute_command(self, command, target, parameters_uri, parameters, profile):
        return super().execute_command(command, target, parameters_uri, parameters, profile)

