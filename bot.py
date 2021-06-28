import discord
from discord.ext import tasks
import os
import asyncio
import random
import datetime, time
from itertools import cycle

client = discord.Client()
sad_words = ['depressed', "distress", "lonely", "heartbroken", "lost", "pessimistic", "despair", "troubled", "heavyhearted", "disappoint", "miserable", "unhappy", "angry", "sad", "stress"]

status= cycle(["Legends of zelda Majora's mask 3D","Legends of zelda Ocarina of Time 3D", "Legends of zelda Breath of the wild", "Hyrule Warriors: Age of Calamity" ])

encouragements_list = ["You aren't alone, here's cheering \n https://tenor.com/view/link-cheer-gif-11489113", "hang in there!\n https://tenor.com/view/link-gif-7568005", "you're fabulous person!\n https://tenor.com/view/link-fab-fabulous-zelda-gif-8431296", "cheer up dude!\n https://tenor.com/view/link-zelda-wind-waker-cheering-gif-6238607", "You're a better person!\n https://tenor.com/view/link-thumbs-up-approve-like-anime-gif-11291500"]

authourized_users = ["Yassine kharrat#7657"]

i = int(2)
should_encouraging = True

@client.event
async def on_ready():
  change_status.start()
  print("We have logged in as {}".format(client.user))

@tasks.loop(seconds=7200)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_message(mess):
  global should_encouraging, authourized_users
  welcome_message = "Hi there!\n I'm your friendly-neighbourhood Link, I'll help you in your quest by encouraging you and reminding you of any event like meeting :D\n Nice to meet you all!\nhttps://tenor.com/view/link-zelda-hyrule-warriors-legend-of-zelda-gif-12193691"
   
  
  enco= random.choice(encouragements_list)
  msg = mess.content

  if mess.author == client.user:
    return
  elif mess.content.startswith("!link"):
    await mess.channel.send(welcome_message)
  
  #embed functions
  elif msg.startswith("!help"):
    embed = discord.Embed(title="Help commands", description= "My helpful commands", colour=discord.Color.green())
    embed.add_field(name="!link", value="My introduction")
    embed.add_field(name="!remind", value="Set a reminder, only one reminder at a time ")
    embed.add_field(name="!switch_enco", value="enable or disable the encouraging messages but right now, only my dad can do it!")
    await mess.channel.send(content=None, embed=embed)    

  elif msg.startswith("!remind"):
      current_time = datetime.datetime.now()
      Date = current_time.strftime("%d/%m/%Y")
      Hour, Minutes = int(current_time.hour + 1) *3600  , int(current_time.minute) * 60
      extract_msg_time, extract_msg_day, cause  = msg.split(",",3)[-1], msg.split(",",3)[2], msg.split(",",3)[1]
      extract_msg_time = extract_msg_time.replace(" ", "")
      extract_hour, extract_minute = int(extract_msg_time.split(":", 2)[0]) * 3600, int(extract_msg_time.split(":", 2)[1]) * 60 
      extract_seconds = extract_hour + extract_minute
      seconds = -(Hour +Minutes) + (extract_seconds)
      #before waiting
      await mess.channel.send("{} scheduled a reminder about {} at {}.".format(mess.author,cause, extract_msg_time))
      #the waiting
      await asyncio.sleep(seconds)
      #after the waiting
      await mess.channel.send("'@everyone,we have {} at {}'-{}".format(cause, extract_msg_time, mess.author))

  elif msg.startswith("!list_reminders"):
    return

  elif any(words in msg.lower() for words in sad_words):
    if should_encouraging:
      await mess.channel.send(enco)
    else: 
      print("not encouraging :I *sad hyaa!*")

  elif msg.startswith("!switch_enco") and str(mess.author) in authourized_users:
    if should_encouraging:
      await mess.channel.send("no more encouraging\nhttps://tenor.com/view/link-legend-of-zelda-hyrule-warriors-gif-8757627")
      should_encouraging = False
    else:
      await mess.channel.send("I'll keep on encouraging people\n https://tenor.com/view/link-wolf-zelda-gif-11809812")     
      should_encouraging = True
    print(should_encouraging) 
  else:
    print("{} tried to do {} in channel".format(mess.author, msg, mess.channel))
      

client.run(os.getenv("TOKEN"))