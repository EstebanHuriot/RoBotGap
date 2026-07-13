import asyncio
import discord

import credentials as cr
from bot.audio import play_death_sound
from gapi.live_client_api import LiveClientAPI
from gapi.live_events import event_monitoring

# Global ATM, will change it later on
crew = [cr.game_name]
data = []
last_event_id = -1

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

    if message.author.bot: # bot ne de déclenche pas lui même
        return

    if message.content.lower() == 'hello':
        channel = message.channel
        await channel.send('Hello')

    if message.content.lower() == 'test':
        author = message.author
        await author.send('I know what you are hiding')




async def monitoring_loop():
    """ 
    This functions makes the link from the event monitoring in the live client API and the discord bot.
    Events are created with event_monitoring() and the functions that trigger the bots are used accordingly.
    """

    
    await bot.wait_until_ready()
    
    global last_event_id, data

    while True:
        try:
            response = LiveClientAPI().get_live_data()
            if "ok" in response :
                print(response)
                break
            

            last_event_id, data, p = await event_monitoring(crew=crew,response=response ,last_event_id=last_event_id ,data=data,)   

            if p is True:
                await play_death_sound(bot=bot, guild_id=cr.guild_id, voice_channel_id=cr.voc_channel_id)


        except Exception as error:
            print("Erreur pendant le monitoring :", error)

        await asyncio.sleep(1)


async def main():
    async with bot:
        # Starting monitoring as a parallel task
        monitoring_task = asyncio.create_task(monitoring_loop())

        try:
            # starting the bot and staying active while the bot is up
            await bot.start(cr.discord_bot_token)

        finally:
            # if bot stops, monitoring stops
            monitoring_task.cancel()




