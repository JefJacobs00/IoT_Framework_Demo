from plugins.tool import Tool


class Gobuster(Tool):
    def __init__(self):
        parser = {'page': '2K', 'status': 'Status: ', 'size': 'Size: ', 'redirect': '--> '}
        line_start = '\['
        super().__init__(parser=parser, info_start=line_start)

    def execute_command(self, command, target):
        return super().execute_command(command, target)

    # def enum_vhost(self, hostnames, port):
    # 	  flags = '-r'
    #     # print(hostnames)
    #     for h in hostnames:
    #         hostname = h['name']
    #         type = 'vhost'
    #         wordlist = 'wordlists/subdomains-top1million-5000.txt'
    #         return self.perform_enum(hostname, port, type, wordlist, self.flags_vhost)
