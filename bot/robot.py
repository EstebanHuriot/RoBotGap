import asyncio
import discord

import credentials as cr
from bot.audio import play_sound, connect_to_vc
from gapi.live_client_api import LiveClientAPI
from gapi.live_events import event_monitoring

# Global ATM, will change it later on
crew = [cr.game_name]
data = []
last_event_id = -1
monitoring_task = None

bot = discord.Client(intents=discord.Intents.all()) # gives all permissions to the bot


@bot.event
async def on_ready():
    serv = cr.discord_channel # guild or server id
    chan = cr.discord_salon_vocal # channel id 

    print(f"Bot connecté : {bot.user}")

    guild = bot.get_guild(serv)
    channel = bot.get_channel(chan)

    print("Serveur :", guild)
    print("Salon :", channel)


@bot.event
async def on_message(message: discord.Message):
    global monitoring_task

    if message.author.bot: # bot ne de déclenche pas lui même
        return

    if message.content.lower() == 'hello':
        channel = message.channel
        await channel.send('Hello')

    if message.content.lower() == 'test':
        author = message.author
        await author.send('I know what you are hiding')

    if message.content.lower() == '!monitoring':
        
        if monitoring_task is None or monitoring_task.done():
            monitoring_task = asyncio.create_task(monitoring_loop())
            
        else:
            await message.channel.send("Le monitoring est déjà actif.")
        




async def monitoring_loop():
    """ 
    This functions makes the link from the event monitoring in the live client API and the discord bot.
    Events are created with event_monitoring() and the functions that trigger the bots are used accordingly.
    """
    print('started')
    
    await bot.wait_until_ready()

    print('bot ready')
    
    global last_event_id, data

    while True:
        try:
            response = LiveClientAPI().get_live_data()
            if "ok" in response :
                print(response)
                # break
                await asyncio.sleep(5)
                continue

            last_event_id, data, game_start, k, d, a = await event_monitoring(crew=crew,response=response ,last_event_id=last_event_id ,data=data)   

            # connects the bot to the vocal if the game has started
            if game_start:
                await connect_to_vc(bot=bot, guild_id=cr.guild_id, voice_channel_id=cr.voc_channel_id)

            # crew member kills
            if k is True:
                await play_sound(bot=bot, guild_id=cr.guild_id, voice_channel_id=cr.voc_channel_id, sound_event="kill")

            # crew member dies
            if d is True:
                await play_sound(bot=bot, guild_id=cr.guild_id, voice_channel_id=cr.voc_channel_id, sound_event="death")

            # crew member assists
            if a is True:
                await play_sound(bot=bot, guild_id=cr.guild_id, voice_channel_id=cr.voc_channel_id, sound_event="assist")


        except Exception as error:
            print("Erreur pendant le monitoring :", error)

        await asyncio.sleep(1)


async def main():
    async with bot:
            
        # starting the bot and staying active while the bot is up
        await bot.start(cr.discord_bot_token)

