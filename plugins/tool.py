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
    def execute_command(self, command, target, parameters_uri, parameters, profile):
        scan = {'ipv4': target, 'profileName': profile, 'command': command.decode('utf8'), 'epochTime': time.time()}
        self.print_scan(scan)
        scan_info = []
        for parameter in parameters_uri:
            info = {'ParameterURI': parameter}
            for key in scan:
                info[key] = scan[key]
            scan_info.append(info)

        self.ontology.putOutputIntoOntology(scan_info, parameters)
        self.ontology.saveToFile('ontology/knowledgebase.ttl')

        start_time = time.time()
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
        (output, err) = p.communicate()
        end_time = time.time()
        output_parser = OutputParser()
        result = output_parser.parse(output.decode("utf-8"), self.parser, self.info_start, self.info_end)
        if len(result) > 0:
            print("Results: ")
            res_str = ""
            for r in result:
                if len(r) > 0:
                    res_str += "\n"
                for x in r:
                    if not self.check_result(r[x], parameters):
                        res_str += f"\t{x}: {r[x]} \n"
            print(res_str)

        self.link_scan(result, scan)
        for r in result:
            for parameter in parameters:
                r[parameter] = parameters[parameter]
            r['duration'] = round((end_time - start_time) * 1000, 2)
            r['executionTime'] = datetime.datetime.now().strftime('%H:%M %d/%m/%Y')

        self.write_output(f'./ScanOutputs/{profile}_{datetime.datetime.now()}', output)
        return result

    def print_scan(self, scan):
        scan_title = f"Executing {scan['profileName']} with the command"
        x = len(scan["command"]) - (len(scan_title) + 2)
        title_filling = '-' * (10 if x < 0 else x//2)
        total = f"{title_filling} {scan_title} {title_filling}"
        print(total)
        print(f"\n\t{scan['command']}\n")
        print(f"{'-'*len(total)}")


    def check_result(self, value, parameters):
        if value == "":
            return True
        for key in parameters:
            if parameters[key] == value:
                return True
        return False
    def link_scan(self, result, scan):
        for r in result:
            for s in scan:
                r[s] = scan[s]

    @staticmethod
    def write_output(path, output):
        with open(path, 'w') as file:
            file.write(output.decode("utf-8"))
