from subprocess import Popen, PIPE

class Hydra:
    def __init__(self, ontology):
        self.ontology = ontology

    def brute_hydra_ssh(self, host, port):
        # print('running hydra')
        wordlist = f'wordlists/default_credentials/ssh.txt'
        # wordlist = f'wordlists/default_credentials/common2.txt'
        cmd = f'hydra -C {wordlist} {host} -s {port} -t 4 ssh'

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8")
        print(output, err)

