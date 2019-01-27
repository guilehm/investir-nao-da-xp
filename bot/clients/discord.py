from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from discord.ext import commands

from xp.settings import CHATTERBOT, DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix='.')
bot = ChatBot(**CHATTERBOT)
messages = [
    'oi', 'olá', 'tudo bem?', 'tudo bem!', 'como vai?', 'como foi seu dia?', 'qual seu nome?', 'vamos jogar?',
    'o que você está fazendo?', 'peidei', 'noob', 'eu te amo', 'quantos anos vocẽ tem?', 'eu jogo Fortnite',
    'quantos anos você tem?', 'o que você faz?', 'eu te odeio', 'vaza daqui', 'infeliz', 'idiota', 'desgraça',
    'aff', 'menos, por favor', 'cala a boca', 'fica quieto', 'burro', 
]


trainer = ListTrainer(bot)
trainer.train(messages)


@client.event
async def on_ready():
    print('Bot está pronto :)')


@client.event
async def on_message(message):


    channel = message.channel

    if message.content.startswith('.conversar'):
        raw_content = message.content.split()
        content = ' '.join(raw_content[1:])
        output = bot.get_response(content)
        await client.send_message(channel, output)

    if message.content.startswith('.ping'):
        await client.send_message(channel, 'pong! :D')

    if message.content.startswith('.fala'):
        msg = message.content
        output = msg.strip('.fala ')
        await client.send_message(channel, output)


client.run(DISCORD_BOT_TOKEN)
