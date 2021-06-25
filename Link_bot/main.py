import discord
import os
import asyncio
import random
import datetime, time
from replit import db
from keep_alive import keep_alive

client = discord.Client()
sad_words = ['depressed', "distressed", "lonely", "heartbroken", "lost", ":frowning:", "pessimistic", "despair", "troubled", "heavyhearted", "disappointed", "miserable", "unhappy", "angry", "sad", "stressed"]

encouragements_list = ["You aren't alone, here's cheering \n https://tenor.com/view/link-cheer-gif-11489113", "hang in there!\n https://tenor.com/view/link-gif-7568005", "you're fabulous person!\n https://tenor.com/view/link-fab-fabulous-zelda-gif-8431296", "cheer up dude!\n https://tenor.com/view/link-zelda-wind-waker-cheering-gif-6238607", "You're a better person!\n https://tenor.com/view/link-thumbs-up-approve-like-anime-gif-11291500"]
i = int(2)
should_encouraging = True

@client.event
async def on_ready():
  print("We have logged in as {}".format(client.user))

@client.event
async def on_message(mess):
  global i, should_encouraging
  welcome_message = "Hi there!\n I'm your friendly-neighbourhood Link, I'll help you in your quest by encouraging you and reminding you of any event like meeting :D\n Nice to meet you all!\ncommands:\n!remind,{event_name}, {Date}, {Time} --> set a reminder.\n!link --> hear my hyaaa!\n !switch_enco -->enable/disable encouragements \nhttps://tenor.com/view/link-zelda-hyrule-warriors-legend-of-zelda-gif-12193691"
   
  
  enco= random.choice(encouragements_list)
  msg = mess.content

  if mess.author == client.user:
    return
  elif mess.content.startswith("!link"):
    if i <= 4:
      await mess.channel.send("Hyaaa!")
      i= i+ 1
    else :
      await mess.channel.send("Hyaaa!! **intensifies**")

  elif msg.startswith("!help"):
    await mess.channel.send(welcome_message)

  elif msg.startswith("!remind"):
      current_time = datetime.datetime.now()
      Date = current_time.strftime("%d/%m/%Y")
      Hour, Minutes = int(current_time.hour + 1) *3600  , int(current_time.minute) * 60
      extract_msg_time, extract_msg_day, cause  = msg.split(",",3)[3], msg.split(",",3)[2], msg.split(",",3)[1]
      extract_msg_time = extract_msg_time.replace(" ", "")
      extract_hour, extract_minute = int(extract_msg_time.split(":", 2)[0]) * 3600, int(extract_msg_time.split(":", 2)[1]) * 60 
      extract_seconds = extract_hour + extract_minute
      seconds = -(Hour +Minutes) + (extract_seconds)
      #before waiting
      await mess.channel.send("{} scheduled a reminder about {} at {} on {}".format(mess.author,cause, extract_msg_time, extract_msg_day))
      #the waiting
      await asyncio.sleep(seconds)
      #after the waiting
      await mess.channel.send("'@everyone,we have {} at {}'-{}".format(cause, extract_msg_time, mess.author))

  elif msg.startswith("!list_reminders"):
    return

  elif msg.startswith("!switch_enco"):
    if should_encouraging:
      await mess.channel.send("no more encouraging\nhttps://tenor.com/view/link-legend-of-zelda-hyrule-warriors-gif-8757627")
      should_encouraging = False
    else:
      await mess.channel.send("I'll keep on encouraging people\n https://tenor.com/view/link-wolf-zelda-gif-11809812")     
      should_encouraging = True
    print(should_encouraging) 
      


  if any(words in msg.lower() for words in sad_words):
    if should_encouraging:
      await mess.channel.send(enco)
    else: 
      print("not encouraging :I *sad hyaa!*")

keep_alive()
client.run(os.getenv("TOKEN"))
