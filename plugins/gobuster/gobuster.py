from subprocess import Popen, PIPE
import re

from plugins.outputParser import OutputParser


class Gobuster():
    def __init__(self):
        self.parser = {'page': '2K', 'status': 'Status: ', 'size': 'Size: ', 'redirect': '--> '}
        self.lineStart = '\['

    def execute_command(self, command, target):
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8")
        if len(err) > 0:
            print(err)
        outputParser = OutputParser()
        return outputParser.stringParse(output, self.parser, self.lineStart)

    # def enum_vhost(self, hostnames, port):
    # 	  flags = '-r'
    #     # print(hostnames)
    #     for h in hostnames:
    #         hostname = h['name']
    #         type = 'vhost'
    #         wordlist = 'wordlists/subdomains-top1million-5000.txt'
    #         return self.perform_enum(hostname, port, type, wordlist, self.flags_vhost)
