import re
class OutputParser:


    def parse(self, input:str, mapping, info_start='', info_end='\n'):
        if isinstance(mapping, dict):
            return self.stringParse(input, mapping, info_start)
        elif isinstance(mapping, re.Pattern):
            return self.stringParseMatcher(input, mapping, info_end)

    def stringParse(self, input:str, mapping, info_start:str):
        lines = re.findall(f'{info_start}.*', input)
        result = []
        for i in range(len(lines)):
            result.append({})
            for key in mapping:
                matches = re.findall(f'({mapping[key]})([a-zA-Z0-9.@/_!-$]+)', lines[i])
                for item in matches:
                    result[i][key] = item[1]
        return result

    def stringParseMatcher(self,input:str, matcher, line_end):
        lines = re.split(line_end, input)
        list = []
        for line in lines:
            result = matcher.search(line)
            if result is not None:
                list.append(result.groupdict())
        return list
