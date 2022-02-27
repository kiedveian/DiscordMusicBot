

import sys

import youtube_dl
from Utility.MusicManager import YTDLSource
from Utility.Utility import ReturnData


music_url = "https://music.youtube.com/watch?v="
youtube_url = "https://www.youtube.com/watch?v="


class YoutubeManager:
    lastData = ''

    def CreateUrl(source, isMusic, start):
        pos = -1
        if isMusic:
            pos = source.find(music_url)
        if pos == -1:
            pos = source.find(youtube_url)
        if pos == -1:
            if isMusic:
                url = music_url + source[start:]
            else:
                url = youtube_url + source[start:]
        else:
            url = source[start:]
        return url

    async def GetDataFromUrl(url, loop=None, steam=True):
        try:
            return await YTDLSource.FromUrl(url, loop=loop, stream=steam)
        except youtube_dl.utils.DownloadError as err:
            exception = err.exc_info
            return ReturnData(False, message='下載失敗: '+str(exception[1]), exception=exception)
        except:
            exception = sys.exc_info()
            return ReturnData(False, log=str(exception[1]), exception=exception)
