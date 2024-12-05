import discord
import os
import heapq
import random
from discord.ext import commands
import json  # Import the JSON module

# Load data from JSON file if it exists, otherwise initialize an empty dictionary
if os.path.exists("data.json"):
    with open("data.json", "r") as f:
        data = json.load(f)
else:
    data = {}

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

losses = {}
for player in data:
    for opp,s1,s2,date in data[player]:
        losses.setdefault(opp,[]).append((player,s2,s1,date))
# print(losses)


@client.event
async def on_ready():
    print("Bot is online")





@client.command()
async def allcmds(ctx):
    await ctx.send("``.addgame <player1> <player2> <score1> <score2> <date> - Add a game to the data``")
    await ctx.send("``.results <player> - Get the results of a player's wins``")
    await ctx.send("``.results all - Get the results of all players' wins``")
    await ctx.send("``.defeats <player> - Get the defeats of a player``")
    await ctx.send("``.remove <player1> <player2> <score1> <score2> <date> - Remove a game from the data``")
    await ctx.send("``.lb wins - See the wins leaderboard``")
    await ctx.send("``.lb defeats - See the defeats leaderboard``")
    await ctx.send("``.kd <player> none - Get the K/D of a player``")
    await ctx.send("``.kd <player1> <player2> - Get the K/D of two players``")
    await ctx.send("``.shutdown - Save data and shut down the bot``")







@client.command()

async def addgame(ctx, p1, p2, s1:int,s2:int,date:str):
   
    if s1 > s2:
        data.setdefault(p1, []).append((p2, s1, s2,date))
        await ctx.send("``logged: " + p1 + " beat " + p2 + " " + str(s1) + "-" + str(s2)+" on "+date+"``")
    elif s1 < s2: 
        data.setdefault(p2, []).append((p1, s2, s1,date))
        await ctx.send("``logged: " + p2 + " beat " + p1 + " " + str(s2) + "-" + str(s1)+" on "+date+"``")





@client.command()
async def results(ctx, p1):
    if p1 == "all":
        
        for player,opps in data.items():
            await ctx.send(f"``{player} beat: ``")
            for opp, s1,s2, date in opps:
                await ctx.send(f"``{opp} {s1}-{s2} on {date}``")
                
                
           
            

    else:
        result = data.get(p1, [])
        if result == []:
            await ctx.send("``none``")
            return
        for opp, s1, s2,date in result:
            await ctx.send("``"+p1 + " beat " + opp + " with a score of " + str(s1) + "-" + str(s2)+" on "+date+"``")



@client.command()
async def defeats(ctx,p1):
    result = losses.get(p1, [])
    if result == []:
        await ctx.send("``none``")
        return
    for opp, s1, s2,date in result:
        await ctx.send("``"+p1 + " lost to " + opp + " with a score of " + str(s1) + "-" + str(s2)+" on "+date+"``")
    



@client.command()
async def remove(ctx, p1, p2, s1:int, s2:int, date:str):
    
    if s1 > s2:
        
        data[p1].remove([p2, s1, s2,date])
        await ctx.send("``removed game: " + p1 + " beat " + p2 + " " + str(s1) + "-" + str(s2)+" on "+str(date)+"``")
        
    if s2 > s1:
        data[p2].remove([p1, s2, s1,date])
        await ctx.send("``removed game: " + p2 + " beat " + p1 + " " + str(s2) + "-" + str(s2)+"``")






@client.command()
async def play(ctx, name):
    a = random.randint(0, 100)
    await ctx.send("``there is a " + str(a) + "% chance you will beat " + name+"``")


@client.command()
async def lb(ctx, type):
    queue = []
    if type == "wins":
        for player in data:
            wins = len(data[player])
            heapq.heappush(queue, (wins*-1, player))
            
    
        counter = 1
        if queue == []:
            await ctx.send("``none``")
        while queue:
            
            wins,player = heapq.heappop(queue)
            wins *= -1
            await ctx.send(f"``{counter}. {player} with {wins} wins``")
            counter += 1
    elif type == "defeats":
        for player in losses:
            loss_count = len(losses[player])
            heapq.heappush(queue, (loss_count*-1, player))


        counter = 1
        if queue == []:
            await ctx.send("``none``")
        while queue:

            loss_count,player = heapq.heappop(queue)
            loss_count *= -1
            await ctx.send(f"``{counter}. {player} with {loss_count} defeats``")
            counter += 1
    # elif type == "kd":
        
        
        



@client.command()
async def kd(ctx, p1, p2):
    if p2 == "none":
        try:
            loss_count = len(losses[p1])
        except:
            loss_count = 0
        try:
            win_count = len(data[p1])
        except:
            win_count = 0
        await ctx.send(f"``the k/d of {p1} is {win_count}/{loss_count}``")
    else:
        p1wins = 0
        for opp,s1,s2,date in data.get(p1,[]):
            if opp == p2:
                p1wins+=1
                    
        p2wins = 0
        for opp,s1,s2,date in data.get(p2,[]):
            if opp == p1:
                p2wins+=1
                
        await ctx.send(f'``the k/d of {p1} vs {p2} is {p1wins}/{p2wins}``')
            





# Save data to JSON file before bot shuts down
@client.event
async def on_disconnect():
    with open("data.json", "w") as f:
        json.dump(data, f)



@client.command()
async def shutdown(ctx):
    await ctx.send("``shutting down...``")
    await client.close()








client.run(os.getenv("TOKEN"))

