import datetime
import math
import time
from abc import abstractmethod, ABC
from subprocess import Popen, PIPE

from plugins.outputParser import OutputParser

class Tool(ABC):
    @abstractmethod
    def __init__(self, ontology, parser='', info_start='', info_end=''):
        self.parser = parser
        self.info_start = info_start
        self.info_end = info_end
        self.ontology = ontology

    @abstractmethod
    def execute_command(self, command, target, profile):
        scan = [{'ipv4': target, 'profileName': profile, 'command': command, 'epochTime': time.time()}]
        self.ontology.putOutputIntoOntology(scan)
        self.ontology.saveToFile('ontology/knowledgebase.ttl')

        start_time = time.time()
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
        (output, err) = p.communicate()
        end_time = time.time()
        output_parser = OutputParser()
        result = output_parser.parse(output.decode("utf-8"), self.parser, self.info_start, self.info_end)
        self.link_scan(result, scan)
        for r in result:
            r['duration'] = round((end_time - start_time) * 1000, 2)
            r['executionTime'] = datetime.datetime.now().strftime('%H:%M %d/%m/%Y')

        self.write_output(f'./ScanOutputs/{profile}_{datetime.datetime.now()}', output)
        return result

    def link_scan(self, result, scan):
        for r in result:
            for s in scan[0]:
                r[s] = scan[0][s]

    @staticmethod
    def write_output(path, output):
        with open(path, 'w') as file:
            file.write(output.decode("utf-8"))
