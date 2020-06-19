import discord

TOKEN = 'NzIzMjI0MTM2NjEyMzE1MjE3.XuvhQw.vqVJ7en1wU2Ba9WNRRYlpBAmLow'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!nanyi'):
        msg = 'Nanyi you are a fucking degenerate!'
        await client.send_message(message.channel, msg)

@client.event   
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

if __name__ == "__main__":
    client.run(TOKEN)