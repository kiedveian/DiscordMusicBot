import time
from Utility.Utility import ReturnData


class VoiceChannelManager:

    def __init__(self) -> None:
        self.voiceClient = None
        self.songList = []
        self.currentSong = None

    async def AddSong(self, channel, song, index=-1, playNow=False):
        if song == None:
            return ReturnData(False, log='[VoiceChannelManager-AddSong] player == None')
        if self.voiceClient == None and channel == None:
            return ReturnData(False, message='找不到語音房')
        if self.voiceClient == None or not self.voiceClient.is_connected():
            self.voiceClient = await channel.connect()
        if index == -1 or index > len(self.songList):
            index = len(self.songList)
        self.songList.insert(index, song)
        if playNow:
            self.PlayNextSong()
        return ReturnData(True, data=index)

    async def Disconnect(self):
        if self.voiceClient == None:
            return
        await self.voiceClient.disconnect()
        self.voiceClient = None

    def PlayNextSong(self, skipNow=False):
        if self.voiceClient == None or not self.voiceClient.is_connected():
            print('[VoiceChannelManager-PlayNextSong] 語音室錯誤')            
            # 自動播放下一首歌不會送錯誤訊息
            return ReturnData(False, message='語音室錯誤')
        if self.voiceClient.is_playing():
            if not skipNow:
                return ReturnData(False, log='[VoiceChannelManager-PlayNextSong is playing')
            self.voiceClient.stop()
        if len(self.songList) <= 0:
            # await self.Disconnect()
            return ReturnData(False, log='[VoiceChannelManager-PlayNextSong list is empty')
        self.currentSong = self.songList[0]
        self.songList = self.songList[1:]
        src = self.currentSong.audioSource
        self.voiceClient.play(src, after=self.OnAfterPlaySingle)
        return ReturnData(True)

    def OnAfterPlaySingle(self, error):
        print("after song")
        if error != None:
            print(error)
        self.currentSong = None
        playData = self.PlayNextSong()
        playData.PrintLog()

    def GetSongList(self):
        return self.songList

    def GetCurrentSongTitle(self):
        if self.currentSong == None:
            return '目前沒有音樂在播放'
        return '目前播放的音樂是' + self.currentSong.info['title']

    def GetSongListTitle(self, start=0, limit=10):
        if len(self.songList) == 0:
            return ReturnData(True, data=[])
        if start < 0 or start >= len(self.songList):
            return ReturnData(False, message='參數錯誤')
        cutList = self.songList[start:]
        if len(cutList) < limit:
            limit = len(cutList)
        else:
            cutList = cutList[:limit]
        data = [(index+start, song.info['title'])
                for index, song in enumerate(cutList)]
        return ReturnData(True, data=data)
