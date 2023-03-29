import re

from plugins.tool import Tool


class Ssh(Tool):
    def __init__(self):
        parser = re.compile(r'')
        super().__init__(parser=parser,info_end='\n')

    def execute_command(self, command, target, profile):
        return