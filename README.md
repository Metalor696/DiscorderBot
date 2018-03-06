# DiscorderBot
Discord implementation of ChatterBot

 I wanted to create a chatbot for Discord and learn Python at the same time so 2 birds one stone!
 
 ## Installation

To start with, Discord and Chatterbot packages need to be installed.

```
pip install chatterbot
pip install discord
```
Alternatively you can get Chatterbot from [PyPi](https://pypi.python.org/pypi/ChatterBot)

MongoDB will also need to be installed. You can get it [Here](https://www.mongodb.com/download-center?jmp=nav#community)
 
 
Next you'll need to add a bot to your Discord server and also create a Bot User for your server. Follow the steps in Reactiflux's Wiki to do this [Creating a discord bot & getting a token](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
 
 You will then need to copy your Bot User token from Discord and save the value into your environment variables with the key name 'DISCORD_BOT_KEY'.
 
 Make sure you have mongoDB set up and running then simply run discorderbot.py and start chatting!
 

If you want to add specific Triggers for your bot to respond to you can add or remove these from the 'triggers' variable in the on_ready function. By default this will create a list of triggers based on your bot name.

Note: This is set to read messages from all server channels and add these reponses to the conversation model in your DB. However, the bot will only respond when a user start's a message with one of it's triggers ie. 'Hey BotName How are you?', 'BotName' etc.

![](https://media.giphy.com/media/4QnCOrIAHSUSc/giphy.gif)
