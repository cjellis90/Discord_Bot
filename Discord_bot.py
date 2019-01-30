import discord
import Bot_secrets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import Discord_bot_functions as UD
from discord.ext.commands import Bot
Discord_Bot = Bot(command_prefix="!")


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
sclient = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = sclient.open("Google Sheets Document").Memberships
 
# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)

@Discord_Bot.event
async def on_ready():
    print('Logged in as')
    print(Discord_Bot.user.name)
    print(Discord_Bot.user.id)
    print('------')
    #displays help me message in discord sidebar
    await Discord_Bot.change_presence(game=discord.Game(name='Use !helpme'))
#display message to a new member to discord server
@Discord_Bot.event
async def on_member_join(member):
   await Discord_Bot.send_message(member, "New Member Message Here")
#reads data from backend to determine and display member subscription status
 @Discord_Bot.command(pass_context=True)
async def subscription(ctx):
    #ctx.message.author.name
    memberName = ctx.message.author.name
    member = ctx.message.author
    roleList = member.roles
    rCheck = 0;
    print(member)

    for x in roleList:
      if(x.name == 'Member'):
        cell = sheet.find(memberName)
        cellRow = cell.row
        myList = sheet.row_values(cellRow)
        startDate = myList[1]
        endDate = myList[2]
        rCheck = 1
        msg = "Your subscription began on {}\nYour subscription will end on {}\nThank you for being a part of the Team!".format(startDate, endDate)
        await Discord_Bot.send_message(ctx.message.author, msg)

    if not(rCheck == 1):
       msg = ("You do not currently have access to the members group.\nIf you have recieved the message in error please contact a moderator in order to update your membership information.\nIf you would like to recieve information about the membership please type !memberinfo")
       await Discord_Bot.send_message(ctx.message.author, msg) 
#displays subscription information
@Discord_Bot.command(pass_context=True)
async def memberinfo(ctx):
   msg = "Input member subscription information here"
   
   await Discord_Bot.send_message(ctx.message.author, msg)
#command takes in two values and returns percent difference
@Discord_Bot.command()
async def profit(val1, val2):
    if(UD.isFloat(val1) and UD.isFloat(val2) and float(val1) > 0 and float(val2) > 0):
       test1 = float(val2) - float(val1)
       finalVal = test1/float(val1) * 100
    
       returnVal = str("%.2f" % finalVal)+"%"
    
       return await Discord_Bot.say(returnVal)
    else:
       return await Discord_Bot.say("The correct format is !profit <Starting Value> <End Value>  Values must be positive numbers")
#takes in value and calculates common percantage goals
#strange spacing is for pretty discord comments
@Discord_Bot.command()
async def entry(value):

    if(UD.isFloat(value)):
      if(float(value) < 0.0):
        return await Discord_Bot.say("Please enter a positive value")
      value = float(value)*.00000001
      onep = UD.percentage(1,value)+value
      twop = UD.percentage(2,value)+value
      threep = UD.percentage(3,value)+value
      fourp = UD.percentage(4,value)+value
      fivep = UD.percentage(5,value)+value
      tenp = UD.percentage(10,value)+value
      fifteenp = UD.percentage(15,value)+value
      twentyp = UD.percentage(20,value)+value
      twentyfivep = UD.percentage(25,value)+value
      thirtyp = UD.percentage(30,value)+value
      Nonep =value-UD.percentage(1,value)
      Ntwop = value-UD.percentage(2,value)
      Nthreep = value-UD.percentage(3,value)
      Nfourp = value-UD.percentage(4,value)
      Nfivep = value-UD.percentage(5,value)
      Ntenp = value-UD.percentage(10,value)
      Nfifteenp = value-UD.percentage(15,value)
      Ntwentyp = value-UD.percentage(20,value)
      Ntwentyfivep = value-UD.percentage(25,value)
      Nthirtyp = value-UD.percentage(30,value)
      return await Discord_Bot.say('```With an entry of {:10.8f} satoshis:\n\n1% = {:10.8f}     10% = {:10.8f}     -1% = {:10.8f}     -10% = {:10.8f}\n\n2% = {:10.8f}     15% = {:10.8f}     -2% = {:10.8f}     -15% = {:10.8f}\n\n3% = {:10.8f}     20% = {:10.8f}     -3% = {:10.8f}     -20% = {:10.8f}\n\n4% = {:10.8f}     25% = {:10.8f}     -4% = {:10.8f}     -25% = {:10.8f}\n\n5% = {:10.8f}     30% = {:10.8f}     -5% = {:10.8f}     -30% = {:10.8f}```'.format(value,onep,tenp,Nonep,Ntenp,twop,fifteenp,Ntwop,Nfifteenp,threep,twentyp,Nthreep,Ntwentyp,fourp,twentyfivep,Nfourp,Ntwentyfivep,fivep,thirtyp,Nfivep,Nthirtyp))
   
    else:
      return await Discord_Bot.say("The correct format is !entry <satoshi price>   You do not need to include leading zero's or a decimal point")
#lists commands to user
@Discord_Bot.command()
async def helpme():
   return await Discord_Bot.say("```!entry <Satoshi price>                  Shows Profit After Entry (Use Satoshis)\n!profit <Starting Value> <End Value>            Calculates Percentage Gain/Loss\n!subscription                                      Check Membership Information\n!memberinfo                             Recieve Information on Membership\n\nThis bot is brand new. More commands are being planned and worked on. If you have any suggestions or comments message a Mod```")




Discord_Bot.run(Bot_secrets.BOT_TOKEN)



