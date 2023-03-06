from plugins.tool import Tool


class Gobuster(Tool):
    def __init__(self):
        parser = {'page': '2K', 'status': 'Status: ', 'size': 'Size: ', 'redirect': '--> '}
        line_start = '\['
        super().__init__(parser=parser, info_start=line_start)

    def execute_command(self, command, target):
        return super().execute_command(command, target)

