import os
import random
from dotenv import load_dotenv

from discord.ext import commands
import asyncio
import emoji

from bs4 import BeautifulSoup

import requests

import discord

from fake_useragent import UserAgent


from datetime import datetime
import pandas as pd
import time
# NzU0Mjg1NzUzNDU0MDM0OTg0.X1yhWQ.a4qGLUjqUJksH7_xWYDsW2jkX0w
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='+')
ua={"UserAgent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    while True:
        await bot.change_presence(activity=discord.Game(name="Ipl 2021"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Ipl21 Live Score"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Ipl21 Schedule"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Ipl21 Next Match"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Ipl21 Point Table"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Ipl21 Comentatry"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Ipl21 Live Score Board"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Spamming"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="Type +help for HELP"))
        await asyncio.sleep(10)


    
   
   

@bot.command(name='hello')
async def stts(ctx):
    await ctx.trigger_typing()
    await ctx.send(f"Namaste {ctx.author.mention}")

def get_score(team):
    flag=0
    tm =""
    ind= 0
    for index , i in enumerate(team):
        if i == ')':
            tm = tm + i
            ind = index
            break
        elif not i.isalpha() and flag==0:
            # print(i)
            tm+="  "+i
            flag = 1
        elif not i.isalpha() and flag==1:
            # print(i)
            tm+=i
        else:
            tm+=i
        # print(tm)
    tm+='\n'
    
    y =team[ind+2:]
    flag = 0
    for index  , i in enumerate(y):
        if not i.isalpha() and flag==0:
            # print(i)
            tm+="  "+i
            flag = 1
        elif not i.isalpha() and flag==1:
            # print(i)
            tm+=i
        else:
            tm+=i
    return tm 
    
         


def get_right(team):
    flag=0
    tm1 =""
    for i in team:
        if i =='(':
            tm1+=" ->  "
            flag=1
        
        if i ==')':
            tm1+=i
            tm1+=' , '
            continue
            
        if not i.isalpha() and flag==0:
            tm1+=" -> "
            flag=1
        tm1+=i
    return tm1 

@bot.command(help='Shows IPL Live Score')
async def ls(ctx):
    await ctx.trigger_typing()

    # url = "https://iplt20api.herokuapp.com/livescore"
    url="https://www.cricbuzz.com/cricket-match/live-scores"
    res = requests.get(url , headers = ua)
    
    
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None,requests.get,url)
    res = await future
    soup = BeautifulSoup(res.content , features='lxml')
    head = soup.findAll(class_='cb-lv-scrs-well-live') #cb-lv-scrs-well-live cb-lv-scrs-well-complete
    if len(head) > 0:
        y =  get_score(head[0].get_text().lstrip())
    else:
        y = "No Current Match Is Running"
    print(y)
    
    embed = discord.Embed(color=0x7e76dc, title='Live Score')
    desc='```arm\n'
    desc+=y+"\n"
    # desc+=tm2+"\n"
    # desc+=status+"\n"
    desc += '```'
    embed.description = desc
    await ctx.send(embed=embed)

    # await ctx.send(head + "\n" + tm1 + "\n"+tm2 + "\n" + status)    

@bot.command()
async def nm(ctx):
    await ctx.trigger_typing()
    url = "https://iplt20api.herokuapp.com/nextmatch"
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, url)
    res = await future
    y = res.json()
    embed = discord.Embed(color=0x7e76dc, title='IPL 2021 Next Match')
    desc='```arm\n'
    desc+= y['Team']+"\n"
    desc+=y['Date']+"\n"
    desc+=y['Time']+"\n"
    desc += '```'
    embed.description = desc
    await ctx.send(embed=embed)

Team_name=['DC', 'CSK','RCB','KKR','KXIP','RR','MI','SRH']

@bot.command(help='Shows IPL Schedule (Add agrue [+sc 2 ,3 , 4..])')

async def sc(ctx , cnt:int):
    await ctx.trigger_typing()
    if cnt >=15:
        return await ctx.send(f"Sorry {ctx.author.mention} I Can Only Respond Upto 17 Count  "+emoji.emojize(":pensive:"))
    url = "https://www.firstpost.com/firstcricket/cricket-schedule/series/ipl-2021.html"
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, url)
    res = await future
    soup = BeautifulSoup(res.content , features='lxml')
    data  =soup.findAll(class_='schedule-head')
    team_name = soup.findAll(class_='sc-match-name')
    time = soup.findAll(class_='sc-label-val')
    tm=0
    day = datetime.now().date().day
    # print(day , "cfdscdfc")
    embed = discord.Embed(color=0xff0000, title='Ipl 2021 Schedule ')
    desc='```\n'
    i = 0
    k = 1
    while k <= cnt:
        if i < len(data) and i <len(team_name) and tm < len(time):
            y = data[i].get_text().strip()
            y = y.replace('\n' , ' ')
            y = y.replace('\t' , '')
            y = y[:6]
            # print(y.split(' ')[0],'decfdcdffvfd')
            p = time[tm].get_text().strip()
            p = p.replace('\n' , ' ')
            p = p.replace('\t' , '')
            r = time[tm+1].get_text().strip()
            r = r.replace('\n' , ' ')
            r = r.replace('\t' , '')
            tm=tm+2
            if int(y.split(' ')[0]) >= int(day):
                k = k+1
                desc+=team_name[i].get_text().strip()+'\n'+p+"  "+r+" "+y+"\n\n"
                # print(k)
                if k <= cnt:
                    desc+='```'+'```'+'\n\n'
            i = i+1
          
    desc += '```'
    embed.description = desc
    await ctx.send(embed=embed)



@bot.command(help='Shows IPL point table')
async def pt(ctx):
	await ctx.trigger_typing()
	url = 'https://www.espncricinfo.com/series/ipl-2021-1249214'
	loop = asyncio.get_event_loop()
	future = loop.run_in_executor(None, requests.get, url)
	res = await future
	soup = BeautifulSoup(res.content , features='lxml')
	points = soup.findAll(class_='pr-3')
	team = soup.findAll(class_='text-left')
	teams=[]
	for i in range(1 , 9):
		teams.append(team[i].get_text())
	match =[]
	win=[]
	loss=[]
	point=[]
	nr=[]
	flag = 0
	for i in range(5 , 45):
		y = points[i].get_text()
		if flag == 0:
			match.append(y)
			flag=1
			continue
		if flag ==1:
			win.append(y)
			flag=2
			continue
		if flag == 2:
			loss.append(y)
			flag=3
			continue
		if flag ==3:
			point.append(y)
			flag=4
			continue
		if flag == 4 :
			nr.append(y)
			flag=0

	embed = discord.Embed(color=0x7e76dc, title='IPL 2021 Point Table')
	desc='```arm\n'
	desc+='Team  Match  Win  Loss  Point   NRR\n'
	desc+='----  -----  ---  ----  -----  -----\n'
	for i in range(0, 8):
		if (nr[i][0] == '-' and len(nr[i]) == 5) or len(nr[i]) == 4:
			nr[i] += '0'
		desc += teams[i] + ' ' * (9 - len(teams[i]) - len(match[i]))
		desc += match[i] + ' ' * (6 - len(win[i]))
		desc += win[i] + ' ' * (6 - len(loss[i]))
		desc += loss[i] + ' ' * (6 - len(point[i]))
		desc += point[i] + ' ' * (9 - len(nr[i])) + nr[i] + '\n'
	desc += '```'
	embed.description = desc
	await ctx.send(embed=embed)

@bot.command(help='Spam Six')

async def six(ctx):
    await ctx.trigger_typing()
    for i in range(0,15):
        await asyncio.sleep(1)
        await ctx.send(emoji.emojize(":six:")+emoji.emojize(":fire:") , delete_after=25)

@bot.command(help='Spam Four')

async def four(ctx):
    await ctx.trigger_typing()
    for i in range(0,15):
        
        await asyncio.sleep(1)
        await ctx.send(emoji.emojize(":four:"),   delete_after=25)

@bot.command(help='Spam out')

async def out(ctx):
    await ctx.trigger_typing()
    for i in range(0,15):
        
        await asyncio.sleep(1)
        await ctx.send("Out"+" "+emoji.emojize(u'\U0001F625') ,   delete_after=25)

@bot.command(help='Spam Freehit')

async def freehit(ctx):
    await ctx.trigger_typing()
    for i in range(0,15):
        
        await asyncio.sleep(1)
        await ctx.send("Hurray FreeHit"+emoji.emojize(u'\U0001F57A') ,   delete_after=25)

@bot.command(help='For Spamming (+ipl argu)')

async def ipl(ctx , *args):
    await ctx.trigger_typing()
    for i in range(0,15):
        
        await asyncio.sleep(1)
        await ctx.send('{}'.format(' '.join(args)) , delete_after=25)

@bot.command(help='Shows IPL Live Score Board')

async def lb(ctx):
    await ctx.trigger_typing()
    url = "https://www.cricbuzz.com/cricket-schedule/upcoming-series/league"
    
    res = requests.get(url , headers=ua)
    
    soup  =BeautifulSoup(res.content , features='lxml')
    data1 = soup.findAll('div' , {'class':'cb-adjst-lst'})
    y = data1[0].find('a').get('href')
    url1 = 'https://www.cricbuzz.com'+str(y)
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, url1)
    res = await future
    soup = BeautifulSoup(res.content , features='lxml')

    data = soup.findAll(class_='cb-min-inf')
    # print(data)
    embed = discord.Embed(color=0x7e76dc, title="Live Score Board")
    desc='```arm\n'
    for ind , val in enumerate(data):
        
        if ind ==1:
            desc+='\n'+'------------------------------------'
        for  i , k  in enumerate(val) :
            if i == 1 or i == 3:
                desc+="\n"
            desc+="\n"
            for j in k:
                # print(j.get_text() , end=" ")
                desc+=j.get_text()+"   "
    desc += '```'
    embed.description = desc
    # print(desc)
    if desc =='```arm'+"\n"+'```':                
        return await ctx.send("No Current IPL Match Is Going")

    await ctx.send(embed=embed)            

    
@bot.command(help = 'Shows stats')

async def stats(ctx):
    await ctx.trigger_typing()
    url = "https://www.cricbuzz.com/cricket-schedule/upcoming-series/league"
    res = requests.get(url , headers=ua)

    soup  =BeautifulSoup(res.content , features='lxml')
    data1 = soup.findAll('div' , {'class':'cb-adjst-lst'})
    y = data1[0].find('a').get('href')
    url1 = 'https://www.cricbuzz.com'+str(y)
    # print(url1)
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, url1)
    res = await future
    soup = BeautifulSoup(res.content , features='lxml')

    data = soup.findAll(class_='cb-key-st-lst')
    if len(data)==0 :
        return await ctx.send("No Current IPL Match Is Going")
    embed = discord.Embed(color=0x7e76dc, title="Key Stats")
    desc='```arm\n'
    desc+=data[0].get_text()[13:33]+'\n'
    rest = data[0].get_text()[32:].split(':')
    desc+=rest[0]+' : '+rest[1].split(',')[0].strip()+' ,'+rest[1].split(',')[1].strip()[0:7] +'\n'
    desc+=rest[1].split(',')[1].strip()[9:]+' : '+rest[len(rest)-1]+'\n'
    desc += '```'
    embed.description = desc
    await ctx.send(embed=embed) 
# @bot.command(help='Shows IPL Live Comentatry')

# async def cm(ctx):
    
#     await ctx.trigger_typing()
#     url="https://www.espncricinfo.com/series/8048/game/1216533/chennai-super-kings-vs-rajasthan-royals-37th-match-indian-premier-league-2020-21"
#     print(ctx.author.id) 
#     if str(ctx.author.id) != "640108121804636160":
#         return await ctx.send("This Operation is only performed by Owner")  

#     store=""
#     dict1={}
#     while(True):
#         store=""
#         res = requests.get(url , headers=ua)
#         soup = BeautifulSoup(res.content , features='lxml')
#         data = soup.findAll(class_='match-comment-long-text')
#         ball_up = soup.findAll(class_='match-comment-short-text')
#         store+=ball_up[0].get_text()+"\n"
#         store+=data[0].get_text()+"\n"
#         if store in dict1:
#             time.sleep(10)
#             continue
#         dict1[store]=1
#         now = datetime.now().time() # time object
#         now = str(now)
#         embed = discord.Embed(color=0x7e76dc, title="Time ->"+now[:5])
#         desc='```arm\n'
#         desc+= ball_up[0].get_text()
#         desc+="\n"
#         desc+=data[0].get_text()
#         desc += '```'
#         embed.description = desc
#         # print(store)
#         await ctx.send(embed=embed)



bot.run(TOKEN)
