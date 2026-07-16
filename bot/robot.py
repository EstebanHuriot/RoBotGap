import asyncio
import discord

import credentials as cr
from bot.audio import play_sound, connect_to_vc
from gapi.live_client_api import LiveClientAPI
from gapi.live_events import event_monitoring
from bot.crew import Crew, CrewMember

# Global ATM, will change it later on
me = CrewMember(cr.game_name, cr.tag_line)
crew = Crew()
crew.add(me)

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

    # monitoring the situation
    if message.content.lower() == '!monitoring':
        
        if monitoring_task is None or monitoring_task.done():
            monitoring_task = asyncio.create_task(monitoring_loop())
            await message.channel.send("I am now monitoring the situation")
            
        else:
            await message.channel.send("Already monitoring the situation")

    if message.content.lower() == '!monitoring stop':

        if monitoring_task is not None and not monitoring_task.done():
            monitoring_task.cancel()
        
            monitoring_task = None

            await message.channel.send("Monitoring stopped.")
        else:
            await message.channel.send("Monitoring is not active.")


    # add a player to the crew
    if message.content.lower().startswith('!crew add'):
        
        try:
            content = message.content.strip()
            command, action, riot_id = content.split(maxsplit=2)
            pseudo, tagline = riot_id.split("#", maxsplit=1)

            player = CrewMember(pseudo, tagline)
            added = crew.add(player)

            if added:
                await message.channel.send(f"{player.full} added")
            
            else:
                await message.channel.send(f"{player.full} is already in the crew")


        except:
            await message.channel.send(f"Could not add")


    # remove a player from the crew
    if message.content.lower().startswith('!crew remove'):
        
        try:
            content = message.content.strip()
            command, action, riot_id = content.split(maxsplit=2)
            pseudo, tagline = riot_id.split("#", maxsplit=1)

            player = CrewMember(pseudo, tagline)
            removed = crew.remove(player)

            if removed:
                await message.channel.send(f"{player.full} removed")
            
            else:
                await message.channel.send(f"{player.full} was not in the crew")


        except:
            await message.channel.send(f"Bro had to stay")

    # show crew members
    if message.content.lower().strip() == '!crew show':
        await message.channel.send(crew.show())

    
    # find if a certain player is in the crew
    if message.content.lower().startswith('!crew find'):
        
        try:
            content = message.content.strip()
            command, action, riot_id = content.split(maxsplit=2)
            pseudo, tagline = riot_id.split("#", maxsplit=1)

            player = CrewMember(pseudo, tagline)
            await message.channel.send(crew.find(player))

        except:
            await message.channel.send(f"Where is bro")



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
            response = LiveClientAPI().get_live_data_check()
            if response["ok"] is False :
                
                print(response)

                # need to clear last_event_id and data in between games or the bot will start monitoring from n+1 event in this game
                # (n = number of events during the previous games) 
                # didn't work directly in event_monitoring() because the API could still send some data after the reset
                last_event_id = -1
                data.clear()

                await asyncio.sleep(5)
                continue

            last_event_id, data, in_game, k, d, a = await event_monitoring(crew=crew,response=response['data'] ,last_event_id=last_event_id ,data=data)   

            # connects the bot to the vocal if the game has started
            if in_game:
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

