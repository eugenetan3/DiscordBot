import discord
import logging
import os
import sys
from riotwatcher import *



TOKEN = 'NzIzMjI0MTM2NjEyMzE1MjE3.XuvhQw.vqVJ7en1wU2Ba9WNRRYlpBAmLow'

watcher = LolWatcher('RGAPI-466a5779-0de3-423c-b7de-c9088b68ada4')
client = discord.Client()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!op.gg'):
        length = len(message.content)
        content = message.content[6:length].strip().replace(' ', '+')
        print(content)
        link = 'https://na.op.gg/summoner/userName={username}'.format(username = content)
      
        await client.send_message(message.channel, link)
    if message.content.startswith('!rstats'):
        region = 'na1'
        length = len(message.content)
        content = message.content[7:length].strip()
        user = watcher.summoner.by_name(region, content)
        print(user)
        rankedstats = watcher.league.by_summoner(region, user['id'])
        print(rankedstats)
        await client.send_message(message.channel, user)
    

@client.event   
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

if __name__ == "__main__":
    client.run(TOKEN)