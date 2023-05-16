from plugins.tool import Tool

class Ffuf(Tool):
    def __init__(self, ontology):
        self.parserDict = {'http_param_fuzz': {'webParameterName': ' FUZZ: '}, 'http_param_input_fuzz': {"webParameterInput": ' FUZZ: '}}
        self.parser = self.parserDict["http_param_fuzz"]
        line_start = '    *'
        super().__init__(ontology=ontology, parser=self.parser, info_start=line_start)

    def execute_command(self, command, target, parameters_uri, parameters, profile):
        self.parser = self.parserDict[profile]
        return super().execute_command(command, target, parameters_uri, parameters, profile)

