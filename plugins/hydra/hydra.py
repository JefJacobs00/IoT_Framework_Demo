from subprocess import Popen, PIPE

from ontology import ontology
from plugins.outputParser import OutputParser


class Hydra:
    def __init__(self):
        self.parser = {'ipv4': 'host: ',
                               'serviceName': '\]\[',
                               'portNumber': '^\[',
                               'accountUsername': 'login: ',
                               'passwordCleartext': 'password: '}
        self.lineStart = '\[\d+\]'

    def execute_command(self, command, target):
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8")
        if len(err) > 0:
            print(err)
        outputParser = OutputParser()
        return outputParser.stringParse(output, self.parser, self.lineStart)

