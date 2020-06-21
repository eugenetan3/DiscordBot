import discord
import logging
import os
import shlex
import sys
import json
from riotwatcher import *


try:
    CONFIG_PATH = os.environ.get("CONFIG_LOC", "config.json")
    cfgfile = open(CONFIG_PATH)
    config = json.load(cfgfile)
except Exception as error:
    logging.error("Error: unable to open config file: {error}".format(error = error))
    sys.exit(1)

if config is not None:
    BOT_TOKEN = config.get("bot_token", None)
    if BOT_TOKEN is None:
        logging.error("Error: No bot token passed")
        sys.exit(1)
    RIOT_TOKEN = config.get("riot_token", None)
    if RIOT_TOKEN is None:
        logging.error("Error: No riot games API token passed")
        sys.exit(1)
    print(config)


watcher = LolWatcher(RIOT_TOKEN) #Refreshes every 24 hr: https://developer.riotgames.com/
client = discord.Client()
client.bot_token = BOT_TOKEN


async def generate_payload(message):
    payload = None
    content = ""
    if isinstance(message, discord.Message):
        content = message.content
    elif isinstance(message, str):
        content = message
    if content.startswith('!'):
        content = content[1::]
        content = shlex.split(content)
        payload = {
            "command": content[0].lower(),
            "arguments": content[1:],
        }
        if isinstance(message, discord.Message):
            payload["user_id"] = message.author.id
            payload["message_id"] = message.id
            payload["message_channel_id"] = message.channel.id
            payload["is_private"] = isinstance(message.channel, discord.abc.PrivateChannel)
    print(payload)
    return payload




@client.event
async def on_message(message):
    generate_payload(message)
    if message.author.id != client.user.id:
        payload = await generate_payload(message)
        if payload is not None:
            #send to backend server here.
            print(message)
    return
'''
    if message.content.startswith('!kill'):
        msg = "Killing Randobot..."
        await message.channel.send(msg)
        sys.exit(0)

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!op.gg'):
        length = len(message.content)
        content = message.content[6:length].strip().replace(' ', '+')
        print(content)
        link = 'https://na.op.gg/summoner/userName={username}'.format(username = content)
      
        await message.channel.send(link)

    if message.content.startswith('!rstats'):
        region = 'na1'
        length = len(message.content)
        content = message.content[7:length].strip()
        user = watcher.summoner.by_name(region, content)
        print(user)
        rankedstats = watcher.league.by_summoner(region, user['id'])
        print(rankedstats)
        summoner_name = rankedstats[0]['summonerName']
        currentlp = rankedstats[0]['leaguePoints']
        wins = rankedstats[0]['wins']
        losses = rankedstats[0]['losses']
        highesttier = rankedstats[0]['tier']
        divisionrank = rankedstats[0]['rank']
        ratio = (wins / (wins + losses)) * 100
        rankedstatus = "```Summoner Name: {summonername}\nCurrent Rank: {tier} {divisionrank} {lp} lp\nWins: {win}\nLosses: {loss}\nW/L Ratio: {ratio:.2f}%\n```".format(summonername = summoner_name, tier = highesttier, divisionrank = divisionrank, lp = currentlp, win = wins, loss = losses, ratio = ratio)
        await message.channel.send(rankedstatus)
'''

@client.event   
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

if __name__ == "__main__":
    client.run(client.bot_token, bot=True)