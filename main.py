import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from Utility.CommandManager import CommandManager
from Utility.Utility import ReturnData
from Utility.VoiceChannelManager import VoiceChannelManager
from Utility.YoutubeManager import YoutubeManager

# 讀取環境變數
load_dotenv()


instents = discord.Intents.default()

botClient = discord.Client()


gVoiceChannelManager = VoiceChannelManager()


# 調用 event 函式庫
@botClient.event
# 當機器人完成啟動時
async def on_ready():
    print('目前登入身份:', botClient.user)


async def CheckAndPlaySong(channel, commandsList):
    if len(commandsList) < 2:
        return ReturnData(False, code=2)
    currentCommand = commandsList[0].lower()
    songCommands = ['p', 'yt', 'music']
    if currentCommand not in songCommands:
        return ReturnData(False, code=1)
    # isMusic = commandsList[0] == 'music'
    # url = YoutubeManager.CreateUrl(commandsList[1], isMusic, 0)
    if len(commandsList) > 2:
        searchUrl = ' '.join([str(elem) for elem in commandsList[1:]])
    else:
        searchUrl = commandsList[1]
    print("search youtube:", searchUrl)

    if searchUrl == '':
        return ReturnData(False)

    songData = await YoutubeManager.GetDataFromUrl(searchUrl)
    if songData == None:
        return ReturnData(False, message="找不到音樂: " + searchUrl)
    elif songData.success == False:
        return songData
    song = songData.data

    global gVoiceChannelManager
    returnData = await gVoiceChannelManager.AddSong(channel, song, playNow=True)
    if returnData.success:
        data = song.info
        # for key, value in YoutubeManager.lastData.items():
        #     print(key, value)
        index = returnData.data
        msg = '點歌成功 ('+data['display_id']+') in index: '+str(index)
        msg = msg+'\n'+data['title']
        return ReturnData(True, message=msg)
    else:
        if returnData.message == '':
            returnData.message = '播放失敗'
        return returnData


def CheckAndStopVoice(commandsList):
    return len(commandsList) >= 1 and commandsList[0].lower() == 'stop'


def CheckAndGetSongList(commandsList):
    listCommands = ['list', 'songlist']
    if len(commandsList) < 1 or commandsList[0].lower() not in listCommands:
        return None
    global gVoiceChannelManager
    return gVoiceChannelManager.GetSongListTitle()


def ChcekAndGetCurrentSong(commandsList):
    listCommands = ['currentsong']
    if len(commandsList) < 1 or commandsList[0].lower() not in listCommands:
        return None
    global gVoiceChannelManager
    return gVoiceChannelManager.GetCurrentSongTitle()


@botClient.event
async def on_message(message):
    if message.author == botClient.user:
        return

    if len(message.content) <= 0:
        return

    commandsList = CommandManager.Paser(message.content, '!')
    if len(commandsList) == 0:
        return

    if CheckAndStopVoice(commandsList):
        global gVoiceChannelManager
        await gVoiceChannelManager.Disconnect()
        return

    currentResult = ChcekAndGetCurrentSong(commandsList)
    if currentResult != None:
        await message.channel.send(currentResult)
        return

    listResult = CheckAndGetSongList(commandsList)
    if listResult != None:
        if listResult.success:
            msg = ""
            for index, data in enumerate(listResult.data):
                msg += '[{}] {}\n'.format(data[0], data[1])
            if len(listResult.data) == 0:
                msg = '歌單是空的'
            await message.channel.send(msg)
        else:
            await listResult.PrintLog().SendMessage(message.channel)
        return

    channel = None
    if message.author.voice != None:
        channel = message.author.voice.channel
    songResult = await CheckAndPlaySong(channel, commandsList)
    if not songResult.success and (songResult.code == 1 or songResult.code == 2):
        await message.channel.send('指令有誤')
    if songResult != None:
        await songResult.PrintLog().SendMessage(message.channel)
    return

    # channel = message.author.voice.channel
    # print(channel)
    # class discord.Message


botClient.run(os.getenv('TOKEN_MUSIC_BOT'))
