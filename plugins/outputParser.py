import re
class OutputParser:
    def stringParse(self, input:str, mapping, infoStart:str):
        lines = re.findall(f'{infoStart}.*', input)
        result = []
        for i in range(len(lines)):
            result.append({})
            for key in mapping:
                result[i][key] = ""
                matches = re.findall(f'({mapping[key]})([a-zA-Z0-9.@/_-]+)', lines[i])
                for item in matches:
                    result[i][key] = item[1]
        return result

    def stringParseMatcher(self, matcher, lineEnd, input:str):
        lines = re.split(lineEnd, input)
        list = []
        for line in lines:
            result = matcher.search(line)
            if result is not None:
                list.append(result.groupdict())
        return list
