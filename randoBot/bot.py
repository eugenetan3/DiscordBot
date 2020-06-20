import discord
import logging
import os
import sys
from riotwatcher import *



TOKEN = 'NzIzMjI0MTM2NjEyMzE1MjE3.XuvhQw.vqVJ7en1wU2Ba9WNRRYlpBAmLow' 

watcher = LolWatcher('RGAPI-b7e56f43-a0eb-43ac-b615-8411be4e9bb0') #Refreshes every 24 hr: https://developer.riotgames.com/
client = discord.Client()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
@client.event
async def on_message(message):
    if message.author == client.user:
        return

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


@client.event   
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

if __name__ == "__main__":
    client.run(TOKEN)