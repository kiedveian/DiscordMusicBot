
class ReturnData:
    def __init__(self, success, message='', log='', data=None, exception=None, code=0):
        self.success = success
        self.message = message
        self.data = data
        self.exception = exception
        self.code = code
        if log == '':
            self.logs = []
        else:
            self.logs = [log]

    async def SendMessage(self, channel):
        if(self.message != ''):
            await channel.send(self.message)
        return self

    def PrintLog(self):
        for log in self.logs:
            if(log != ''):
                print(log)
        if self.exception != None:
            print(self.exception)
        return self
