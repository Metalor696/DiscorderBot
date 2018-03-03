import discord
import asyncio
import os
import logging
import re

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

DISCORD_BOT_KEY = os.environ.get('DISCORD_BOT_KEY')
print(DISCORD_BOT_KEY)

# Uncomment the following lines to enable verbose logging

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
    print('trying to get response from botty')
    return bot.get_response(content)

async def checkForTriggerMatch(query, triggers):
    for t in triggers:
        print('the trigger is: ' + t)
        if(query.lower().startswith(t)):
            print('in the query loop')
            replying = True
            await removeBotReference(query, t)

async def removeBotReference(query, wordtoRemove):  
    src_str  = re.compile(wordtoRemove, re.IGNORECASE)     
    query  = src_str.sub('', query)
    return query

# Create Discord client - This will wrap our Chatbot and read all input but only send a response if the bot is being spoken to
client = discord.Client()

#set discordBot references to be accessed once ready is fired
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

    botName = client.user.name
    botNameCleaned = ''.join(e for e in botName if e.isalnum())
    botId = client.user.id

    print('botName is '+ botName)
    print('botNameCleaned is '+ botNameCleaned)
    print('botid is ' + str(botId))

    #define trigger terms for our bot
    triggers = [botName, botNameCleaned,'@'+str(botId), 'hey @' +str(botId), 'hey ' +botName, 'hey ' +botNameCleaned, 'hi ' +botName, 'hi ' +botNameCleaned, 'oi ' +botName, 'oi ' +botNameCleaned, '!'+botName, '!'+botNameCleaned]
    triggersLower = [x.lower() for x in triggers]

    print(triggersLower)

@client.event
async def on_message(message):
    #hacky implemenation for now
    botName = client.user.name
    botNameCleaned = ''.join(e for e in botName if e.isalnum())
    botId = client.user.id

    triggers = [botName, botNameCleaned,'@'+str(botId), 'hey @' +str(botId), 'hey ' +botName, 'hey ' +botNameCleaned, 'hi ' +botName, 'hi ' +botNameCleaned, 'oi ' +botName, 'oi ' +botNameCleaned, '!'+botName, '!'+botNameCleaned]
    triggersLower = [x.lower() for x in triggers]


    user = message.author if message.author else message.user
    print('User.name is '+user.name)
    if(user.name != client.user.name):
        replying = False
        queryString = message.content
        print('the query string is' +queryString)

        print('on message the triggersLower are: ')
        print(triggersLower)

        if any(map(queryString.lower().startswith, triggersLower)):
            replying = True
            queryString = await removeBotReference(queryString, triggersLower)
        
        response = await getResponse(queryString)
        print('The response from botty is ')
        print(response)        

        print('replying is ' +str(replying))
        # Here we only reply if replying is set to true
        if replying:
            await client.send_message(message.channel, response)

client.run(DISCORD_BOT_KEY)