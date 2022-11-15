from subprocess import Popen, PIPE

from plugins.outputParser import OutputParser


class Hydra:
    def __init__(self, ontology):
        self.ontology = ontology
        self.parser = {'ipAddress': 'host: ',
                               'protocol': '\]\[',
                               'port': '^\[',
                               'username': 'login: ',
                               'password': 'password: '}
        self.lineStart = '\[\d+\]'

    def brute_hydra_ssh(self, host, port):
        # print('running hydra')
        wordlist = f'wordlists/default_credentials/test.txt'
        # wordlist = f'wordlists/default_credentials/common2.txt'
        cmd = f'hydra -C {wordlist} {host} -s {port} -t 4 ssh'

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8")

        outputParser = OutputParser()
        return outputParser.stringParse(output, self.parser, self.lineStart)

