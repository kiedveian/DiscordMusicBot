
class CommandManager:
    def Paser(string, prefix):
        prefixLength = len(prefix)
        if len(string) <= prefixLength or string[:prefixLength] != prefix:
            return []
        remainString = string[prefixLength:]
        pos = remainString.find(' ')
        if pos == -1:
            return [remainString]
        return remainString.split(' ')
