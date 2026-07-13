import discord
from pathlib import Path

BOT_FOLDER = Path(__file__).resolve().parent
PROJECT_FOLDER = BOT_FOLDER.parent

FFMPEG_PATH = PROJECT_FOLDER / "tools" / "ffmpeg.exe"

EVENT_SOUNDS: dict[str, Path] = {
    "kill": BOT_FOLDER / "sounds" / "death.mp3",
    "death": BOT_FOLDER / "sounds" / "death.mp3",
    "assist": BOT_FOLDER / "sounds" / "death.mp3"
    }


async def connect_to_vc(bot:discord.Client ,guild_id:int, voice_channel_id:int):

    guild = bot.get_guild(guild_id) # server
    if guild is None :
        print('Cant find discord server')
        return

    channel = guild.get_channel(voice_channel_id) # channel
    if channel is None:
        print('Cant find discord channel')
        return

    voice_client = guild.voice_client

    if voice_client is None: # bot is not connected to a voice chat then connects
        voice_client = await channel.connect()

    elif voice_client.channel.id != channel.id: # bot is connected to another voicechat the changes
        await voice_client.move_to(channel)

    return voice_client


async def play_sound(bot:discord.Client ,guild_id:int, voice_channel_id:int, sound_event:str):
    
    voice_client = await connect_to_vc(bot=bot, guild_id=guild_id, voice_channel_id=voice_channel_id)

    if voice_client is None:
        return

    if voice_client.is_playing(): # if already playing a song, stops  (keeping it ??)
        voice_client.stop()

    source = discord.FFmpegPCMAudio(str(EVENT_SOUNDS[sound_event]),executable=FFMPEG_PATH)

    voice_client.play(source)