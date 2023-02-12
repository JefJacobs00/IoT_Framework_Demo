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

    def brute_hydra_ssh(self, host, port):
        # print('running hydra')
        wordlist = f'wordlists/default_credentials/test.txt'
        # wordlist = f'wordlists/default_credentials/common2.txt'
        cmd = f'hydra -C {wordlist} {host} -s {port} -t 4 ssh'

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8")
        if len(err) > 0:
            print(err)
        outputParser = OutputParser()
        return outputParser.stringParse(output, self.parser, self.lineStart)

    def execute_command(self, command, target):
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8")
        if len(err) > 0:
            print(err)
        outputParser = OutputParser()
        return outputParser.stringParse(output, self.parser, self.lineStart)

