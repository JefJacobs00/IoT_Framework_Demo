from plugins.tool import Tool


class Hydra(Tool):
    def __init__(self, ontology):
        parser = {'ipv4': 'host: ',
                           'serviceName': '\]\[',
                           'portNumber': '^\[',
                           'accountUsername': 'login: ',
                           'passwordCleartext': 'password: '}
        line_start = '\[\d+\]'

        super().__init__(ontology=ontology, parser=parser, info_start=line_start)

    def execute_command(self, command, target, parameters_uri, parameters, profile):
        return super().execute_command(command, target, parameters_uri, parameters, profile)

