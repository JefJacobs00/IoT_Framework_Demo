import time
from abc import abstractmethod, ABC
from subprocess import Popen, PIPE

from plugins.outputParser import OutputParser

class Tool(ABC):
    @abstractmethod
    def __init__(self, parser='', info_start='', info_end=''):
        self.parser = parser
        self.info_start = info_start
        self.info_end = info_end

    @abstractmethod
    def execute_command(self, command, target):
        start_time = time.time()
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
        (output, err) = p.communicate()
        end_time = time.time()
        output_parser = OutputParser()
        result = output_parser.parse(output.decode("utf-8"), self.parser, self.info_start,self.info_end)
        for r in result:
            r['ipv4'] = target
            r['profileName'] = 'nmap'
            r['command'] = command
            r['duration'] = (end_time - start_time) * 1000
        return result
