import discord
import asyncio
import os
import logging
import re

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

DISCORD_BOT_KEY = os.environ.get('DISCORD_BOT_KEY')
print(DISCORD_BOT_KEY)

logging.basicConfig(level=logging.INFO)

# Create a new ChatBot instance
bot = ChatBot(
    'DiscorderBot',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance'
        }
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    input_adapter='chatterbot.input.VariableInputTypeAdapter',
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
    database='discorderbot-database'
)
bot.set_trainer(ChatterBotCorpusTrainer)

bot.train("chatterbot.corpus.english")

CONVERSATION_ID = bot.storage.create_conversation()

async def getResponse(content):
    return bot.get_response(content)

## need to re-implement this
async def checkForTriggerMatch(query, triggers):
    for t in triggers:
        if(query.lower().startswith(t)):
            replying = True
            await removeBotReference(query, t)

async def removeBotReference(query, queryToLower, wordList):
    for word in wordList: 
        if(queryToLower.startswith(word)):
            src_str  = re.compile(word, re.IGNORECASE)     
            query  = src_str.sub('', query)
            return query

# Create Discord client - This will wrap our Chatbot and read all input but only send a response if the bot is being spoken to
client = discord.Client()

#set global discordBot references to be accessed once ready is fired
botName = ''
botNameCleaned = ''
botId = 0

triggers = []
triggersLower = []

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    global botName
    botName = client.user.name
    global botNameCleaned
    botNameCleaned = ''.join(e for e in botName if e.isalnum())
    global botId
    botId = client.user.id

    #define trigger terms for our bot
    global triggers
    triggers = [botName, botNameCleaned,'<@'+str(botId)+'>', 'hey <@' +str(botId)+'>', 'hey ' +botName, 'hey ' +botNameCleaned, 'hi ' +botName, 'hi ' +botNameCleaned, 'oi ' +botName, 'oi ' +botNameCleaned, '!'+botName, '!'+botNameCleaned]
    global triggersLower
    triggersLower = [x.lower() for x in triggers]

@client.event
async def on_message(message):
    user = message.author if message.author else message.user
    if(user.name != client.user.name): # Checking that the message is not from our bot - we don't want it replying to itself into infinity!
        replying = False
        queryString = message.content
        queryStringToLower = queryString.lower()

        #check if Bot has been summoned.
        if any(map(queryStringToLower.startswith, triggersLower)):
            replying = True
            queryString = await removeBotReference(queryString, queryStringToLower, triggersLower)
        
        #clean string before persisting to DB
        queryString = queryString.lstrip(" ,.?!;][}{%@$^&*")
        response = await getResponse(queryString)

        # Here we only reply if replying is set to true
        if replying:
            await client.send_message(message.channel, response)

client.run(DISCORD_BOT_KEY)