from subprocess import Popen, PIPE
import re

from plugins.outputParser import OutputParser


class Gobuster():
    def __init__(self):
        self.parser = {'page': '2K', 'status': 'Status: ', 'size': 'Size: ', 'redirect': '--> '}
        self.lineStart = '\['

    def perform_enum(self, host, port, type, wordlist, flags):
        cmd = f'gobuster {type} -u http://{host}:{port} -w {wordlist}'

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8")
        err = err.decode("utf-8")

        outputParser = OutputParser()
        return outputParser.stringParse(output, self.parser, self.lineStart)

    def enum_dir(self, host, port):
        flags = '-x php,html,htm,txt,asp,aspx'
        type = 'dir'
        wordlist = 'wordlists/common.txt'
        return self.perform_enum(host, port, type, wordlist, flags)

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
