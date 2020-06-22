import discord
import logging
import os
import shlex
import sys
import json
import aiohttp
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
    BACKEND_ADDR = config.get("backend_addr", None)
    if BACKEND_ADDR is None:
        logging.error("Error: No backend address given")
        sys.exit(1)
    BACKEND_ADDR_PORT = config.get("backend_addr_port")
    if BACKEND_PORT is None:
        logging.error("Error: No port given")
        sys.exit(1)



watcher = LolWatcher(RIOT_TOKEN) #Refreshes every 24 hr: https://developer.riotgames.com/
client = discord.Client()
client.bot_token = BOT_TOKEN
client.backend_addr = BACKEND_ADDR
client.backend_addr_port = BACKEND_ADDR_PORT


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

    return payload

async def get_reply(url, payload):
    reply = {"response":"", "embed":""}
    try:
        async with client.aiohttp_session.post(url, json=payload) as response:
            if response.status == 200:
                jsonItem = await response.json()
                reply["response"] = jsonItem.get("response", "")
                reply["embed"] = jsonItem.get("embed", "")
    except aiohttp.ClientConnectorError as error:
        logging.warning("Error: unable to open config file: {error}".format(error = error))

    return reply

@client.event   
async def on_ready():
    client.aiohttp_session = aiohttp.ClientSession()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')


@client.event
async def on_message(message):
    generate_payload(message)
    if message.author.id != client.user.id:
        payload = await generate_payload(message)
        if payload is not None:
            #send to backend server here.
            url = "http://" + client.backend_addr + ":"
            url += client.backend_addr_port + "/command/" + payload["command"]
            reply = await get_reply(url, payload)
            response = reply["response"]
            embed = None
            try:
                embed = discord.Embed.from_dict(reply["embed"])
            except Exception as e:
                logging.error("Error parsing the embed {e}")
            if response != "" or embed is not None:
                try:
                    await message.channel.send(response, embed=embed)
                except discord.DiscordException as e:
                    logging.error("Error sending message to discord")
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


if __name__ == "__main__":
    client.run(client.bot_token, bot=True)