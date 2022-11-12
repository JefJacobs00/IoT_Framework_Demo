from subprocess import Popen, PIPE
import re

class Gobuster():
    def __init__(self, ontology):
        self.ontology = ontology

    def perform_enum(self, host, port, type, wordlist, flags):
        cmd = f'gobuster {type} -u {host} -w {wordlist} -t 200 --timeout 5s {flags}'

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8")
        err = err.decode("utf-8")

        result = {}
        if type == 'dir':
            pages = self.parse_enum_dir_output(output, err, host, port)
            if pages:
                result = {'domain': {'name': host, 'content': pages}}

        elif type == 'vhost':
            subdomains = self.parse_enum_vhost_output(output)
            if subdomains:
                result = {}
                result['subdomains'] = []
                for s in subdomains:
                    result['subdomains'].append({'name': s})

        return result

    def enum_dir(self, host, port):
        flags = '-x php,html,htm,txt,asp,aspx'
        type = 'dir'
        wordlist = 'wordlists/common.txt'
        return self.perform_enum(host, port, type, wordlist, flags)

    # def enum_vhost(self, hostnames, port):
    # 	  flags = '-r'
    #     # print(hostnames)
    #     for h in hostnames:
    #         hostname = h['name']
    #         type = 'vhost'
    #         wordlist = 'wordlists/subdomains-top1million-5000.txt'
    #         return self.perform_enum(hostname, port, type, wordlist, self.flags_vhost)


    def parse_enum_dir_output(self, output, err, host, port):
        # print(err)
        # print('Gobuster output: ' + output + 'n\n')
        err_status_code = re.search(r'=>\s(\d+)', err)
        if err_status_code:
            return
        # TODO error handling
        # err = err_status_code.group(0).split()
        # status = int(err[1])
        # # print(status)
        # self.flags_dir += f' -b {status}'
        # # print(self.flags_dir)

        else:
            paths = []
            matches = re.findall(r'(/\w+\.*\w*)\s+\(Status: (\d+)\)\s*\[Size: (\d+)]', output)
            pages = []
            for match in matches:
                url = match[0]
                if url in paths:
                    continue

                if '.' in url:
                    p = url.split('.')[0]
                    if p in paths:
                        continue

                for i, path in enumerate(paths):
                    if '.' in path:
                        p = path.split('.')[0]
                        if p == url:
                            paths.pop(i)

                paths.append(url)
                status = match[1]
                # length = match[2]

                page = {'path': url, 'status': status}
                if page not in pages:
                    pages.append(page)

                # classes needed
                request_type = 'HttpRequest'
                response_type = 'HttpResponse'
                url_type = 'URL'
            return pages

    def parse_enum_vhost_output(self, output):
        matches = re.findall(r'Found: (\w+(\.\w+)+)', output)
        subdomains = []
        for match in matches:
            subdomain = match[0]
            subdomains.append(subdomain)

        return subdomains