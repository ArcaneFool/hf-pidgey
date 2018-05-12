import discord
import random
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import urbandict
from asyncurban import UrbanDictionary
import cassiopeia as cass
import requests
import json
import py_gg


botprefix = ('<', '£', '=', '"')
TOKEN = "NDIwODgyNDc2NzQ4MjQyOTQ0.DZFyFw.81RzMdHOt3XBCLLa5MLZ1n2WTV0"
client = Bot(command_prefix=botprefix)


@client.command(name='8ball',
                pass_context=True
                )
async def ball(context, *, inp):
    if inp == "Are you gay" or inp == "are you gay":
        nou = discord.Embed(title="8Ball", color=0xFFA2F0)
        nou.add_field(name="Question", value=inp, inline=False)
        nou.add_field(name="Response", value="NO YOU", inline=False)
        nou.set_thumbnail(url="https://cdn.emojidex.com/emoji/seal/8ball.png?1417132124")
        nou.set_footer(text="8Ball, The future is predictable",
                       icon_url="http://www.clker.com/cliparts/w/L/F/v/7/8/sparkle-md.png")
        await client.say(context.message.author.mention)
        await client.say(embed=nou)
    else:
        possible_responses = ["FUCK YH", "ARE YOU GAY", "YOUR MUM GAY", "NO RETARD", "NO KYS", "OFC FUCKTARD", "NO YOU",
                              "IL TOUCHA YOUR SPAGHET", "ASK YOUR DICKHOLE"]
        reply = discord.Embed(title="8Ball", color=0xFFA2F0)
        reply.add_field(name="Question", value=inp, inline=False)
        reply.add_field(name="Response", value=random.choice(possible_responses), inline=False)
        reply.set_thumbnail(url="https://cdn.emojidex.com/emoji/seal/8ball.png?1417132124")
        reply.set_footer(text="8Ball, The future is predictable",
                         icon_url="http://www.clker.com/cliparts/w/L/F/v/7/8/sparkle-md.png")
        await client.say(context.message.author.mention)
        await client.say(embed=reply)
    await client.delete_message(context.message)


@client.command(pass_context=True)
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.message.author
    av = member.avatar_url
    if ".gif" in av:
        av += "&f=.gif"
    pic = discord.Embed(title="Avatar", color=0x0062f4)
    pic.set_image(url=str(av))
    pic.set_footer(text=str(member))
    await client.send_message(ctx.message.channel, embed=pic)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
@commands.cooldown(3,5,BucketType.server)
async def summoner(ctx, region, *, nam):
    cass.set_riot_api_key("RGAPI-c475dafe-804f-48f7-9c11-7eccba8b90da")  # This overrides the value set in your configuration/settings.
    try:
        cass.set_default_region(region)
        summoner = cass.get_summoner(name=str(nam))
        good_with = summoner.champion_masteries.filter(lambda cm: cm.level >= 6)
        q = str(summoner.name)
        q = str.title(q)
        x = str(summoner.region)
        x = x[7:]
        x = str.title(x)
        user = nam.replace(' ', '+')
        link = "http://" + region + ".op.gg/summoner/userName=" + user
        icons=summoner.profile_icon.url


        embed = discord.Embed(title="Summoner Info", description="Here's what I could find", color=0xff71ce)
        embed.add_field(name="Summoner Name", value=q, inline=True)
        embed.add_field(name="Summoner Level", value="Level {}".format(summoner.level), inline=True)
        embed.add_field(name="Region", value=x, inline=True)
        embed.add_field(name="Good With (M6 Or Higher)", value=[cm.champion.name for cm in good_with], inline=True)
        embed.add_field(name="OP.GG Link", value=link, inline=True)
        embed.set_footer(text="League of Legends")
        embed.set_thumbnail(url=str(icons))
        await client.say(embed=embed)


    except commands.CommandOnCooldown:
        await client.say("Command is on Cooldown 3 Uses Per 5 Second")
    except Exception as e:
        await client.say("No Summoner Found Or Region Is Wrong!")


@client.command(pass_context=True,
                aliases=["purge", "Purge", "Prune"]
                )
async def prune(context, number):
    number = int(number)
    if context.message.author.server_permissions.manage_messages == True:
        msg = []
        async for x in client.logs_from(context.message.channel, limit=number + 1):
            msg.append(x)
        await client.delete_messages(msg)
        await client.say(str(number) + " Messages Deleted")
    else:
        await client.say("FUCK OUTTA HERE YOU AIN'T NO MODERATOR" + " , " + context.message.author.mention)


@client.command(pass_context=True)
async def urban(ctx, *, word):
    try:
        defi = urbandict.define(word)
        define = defi[0]['def']
        example = defi[0]['example']
        out = discord.Embed(title=str.upper(word), descripition=define, color=0x0062f4)
        out.add_field(name="Meaning", value=str.title(define), inline=False)
        out.add_field(name="Example", value=str.title(example), inline=False)
        out.set_footer(text="Urban Dictionary, " + ctx.message.author.name,
                       icon_url='https://vignette.wikia.nocookie.net/logopedia/images/a/a7/UDAppIcon.jpg/revision/latest?cb=20170422211150')
        out.set_thumbnail(
            url='https://s3.amazonaws.com/pushbullet-uploads/ujxPklLhvyK-RGDsDKNxGPDh29VWVd5iJOh8hkiBTRyC/urban_dictionary.jpg?w=188&h=188&fit=crop')
        await client.send_message(ctx.message.channel, embed=out)
    except Exception as e:
        await client.say(
            "Something Went Wrong, Theres Probably No Definition For This Word On Urban Dictionary, " + ctx.message.author.mention)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def urban_random(ctx):
    urb = UrbanDictionary(loop=client.loop)
    word = str(await urb.get_random())
    defi = urbandict.define(str(word))
    define = defi[0]['def']
    example = defi[0]['example']
    out = discord.Embed(title=str.upper(word), descripition=define, color=0x0062f4)
    out.add_field(name="Meaning", value=str.title(define), inline=False)
    out.add_field(name="Example", value=str.title(example), inline=False)
    out.set_footer(text="Urban Dictionary, " + ctx.message.author.name,
                   icon_url='https://vignette.wikia.nocookie.net/logopedia/images/a/a7/UDAppIcon.jpg/revision/latest?cb=20170422211150')
    out.set_thumbnail(
        url='https://s3.amazonaws.com/pushbullet-uploads/ujxPklLhvyK-RGDsDKNxGPDh29VWVd5iJOh8hkiBTRyC/urban_dictionary.jpg?w=188&h=188&fit=crop')
    await client.send_message(ctx.message.channel, embed=out)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def botrename(ctx, *, name: str):
    if str(ctx.message.author.id) == "241305141624438784":
        await client.edit_profile(username=name)
        await client.say("Done, Bots name changed.")
        await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def ban(ctx, *, member: discord.Member):
    if ctx.message.author.server_permissions.ban_members == True:
        av = member.avatar_url
        if ".gif" in av:
            av += "&f=.gif"
        bas = discord.Embed(title="Banned", description=str(member) + " Was Banned", color=0xF00000)
        bas.set_thumbnail(url=str(av))
        bas.set_footer(text="The Hammer Has Spoken", icon_url="https://d30y9cdsu7xlg0.cloudfront.net/png/1657-200.png")
        try:
            await client.ban(member)
            await client.send_message(ctx.message.channel, embed=bas)
        except discord.errors.Forbidden:
            await client.say(str.title("The bot does not have sufficient permissions!"))
        except Exception as e:
            return
    else:
        await client.say(str.title("You Dont have sufficient permissions!"))
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def kick(ctx, *, member: discord.Member):
    await client.delete_message(ctx.message)
    if ctx.message.author.server_permissions.kick_members == True:
        av = member.avatar_url
        if ".gif" in av:
            av += "&f=.gif"
        bas = discord.Embed(title="Kicked", description=str(member) + " Was Kicked", color=0xF00000)
        bas.set_thumbnail(url=str(av))
        bas.set_footer(text="The Hammer Has Spoken", icon_url="https://d30y9cdsu7xlg0.cloudfront.net/png/1657-200.png")
        try:
            await client.kick(member)
            await client.send_message(ctx.message.channel, embed=bas)
        except discord.errors.Forbidden:
            await client.say(str.title("The bot does not have sufficient permissions!"))
        except Exception as e:
            return
    else:
        await client.say(str.title("You Dont have sufficient permissions!"))
    await client.delete_message(ctx.message)



@client.command(pass_context=True)
async def blob(ctx):
    await client.delete_message(ctx.message)
    await client.say("<a:blobjump:435770313201025025>")


@client.command(pass_context=True)
async def high(ctx):
    await client.delete_message(ctx.message)
    await client.say("<a:pepehigh:436129076789641238>")


@client.command(pass_context=True)
async def cri(ctx):
    await client.delete_message(ctx.message)
    await client.say("<a:cri:441291814641860616>")


@client.command(pass_context=True)
async def hug(ctx):
    await client.delete_message(ctx.message)
    await client.say("<a:Blobhugif:432693055607406602>")


@client.command(pass_context=True)
async def doc(ctx):
    await client.delete_message(ctx.message)
    await client.say("STFU DOC")


@client.command(pass_context=True, aliases=["deus", "vult"])
async def deusvult(ctx):
    await client.say("<:deus:400702195714228254><:vult:400702245529845771>")
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def sing(ctx):
    song = (
        "We're no strangers to love You know the rules and so do I A full commitment's what I'm thinking of You wouldn't get this from any other guy I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you We've known each other for so long Your heart's been aching, but You're too shy to say it Inside, we both know what's been going on We know the game and we're gonna play it And if you ask me how I'm feeling Don't tell me you're too blind to see Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you (Ooh, give you up) (Ooh, give you up) Never gonna give, never gonna give (Give you up) Never gonna give, never gonna give (Give you up) We've known each other for so long Your heart's been aching, but You're too shy to say it Inside, we both know what's been going on We know the game and we're gonna play it I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you")
    my_var = song.split()
    if str(ctx.message.channel) == "spam":
        for word in my_var:
            await client.say(word)
    else:
        await client.say("Command Only Works in Spam Channel" + ctx.message.author.mention)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def oof(ctx):
    await client.delete_message(ctx.message)
    await client.say("OOF")


@client.command(pass_context=True, description="Only Works in Dunder Mifflin Server",
                brief="Only Works in Dunder Mifflin Server")
async def ping(ctx):
    if str(ctx.message.server) == "Dunder Mifflin":
        result = [" is a korean boy loving ass", " is a lolifurry", " likes boy semen", " likes dem wrickled tits",
                  " likes there brothers rod", " IS A DOUCHEBAGGETE", " im jealous of everyone who HASN'T MET YOU",
                  " IS A DOGGYKNOBBER", " licks his mothers minge"]
        mentions = ["<@265851383692001280>", "<@277129203592331264>", "<@241305141624438784>", "<@280443982864056320>",
                    "<@149452733215277056>", "<@174244883970654208>", "<@133028189243965440>", "<@107426138988482560>"]
        await client.say(random.choice(mentions) + random.choice(result))


@client.command(pass_context=True)
async def invite(ctx):
    await client.say(
        "INVITE MY GAY ASS WITH THIS URL" + " " + "https://discordapp.com/oauth2/authorize?client_id=420882476748242944&scope=bot&permissions=939979967" + " , " + ctx.message.author.mention)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def spam(context, count, *, member):
    await client.delete_message(context.message)
    if str(context.message.author) == "Saltysplatoon#2045" and str(context.message.channel) == "spam":
        for i in range(1, 50):
            await client.say("<@280443982864056320>")
    elif str(context.message.channel) == "spam" or context.message.author.server_permissions.ban_members == True:
        for i in range(1, int(count) + 1):
            await client.say(member)
    else:
        await client.say("Only Works in Spam channel/Mod only")


@client.command(pass_context=True)
async def splash(ctx, *, champion):
    original = str.title(champion)
    champion = str.title(champion)
    if champion == "Wukong":
        champion = "MonkeyKing"
    new_champion = champion.replace(' ', '')
    imgurl = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + new_champion + "_0.jpg"
    q = requests.get(imgurl)
    if str(q) == "<Response [200]>":
        embed = discord.Embed(title=original, description="{}'s Splash Art".format(original), color=0x003366)
        embed.set_image(url=imgurl)
        embed.set_footer(text="League of Legends",
                         icon_url="https://vignette.wikia.nocookie.net/leagueoflegends/images/1/12/League_of_Legends_Icon.png/revision/latest?cb=20150402234343")
        await client.say(embed=embed)
    else:
        await client.say("Something Went Wrong Try Again")
    await client.delete_message(ctx.message)

@client.command(pass_context=True)
@commands.cooldown(1,1,BucketType.server)
async def skinid(ctx,*,champ):
    champfirst=champ
    champ=str.title(champ)
    champ=champ.replace(" ","")
    ses= requests.Session()
    txt=ses.get("http://ddragon.leagueoflegends.com/cdn/8.9.1/data/en_US/champion/{}.json".format(champ))
    full_ids=txt.text
    data = json.loads(full_ids.encode('utf-8'))
    urls="https://ddragon.leagueoflegends.com/cdn/8.9.1/img/champion/" + str(data['data'][str(champ)]['image']['full'])
    try:
        embed=discord.Embed(title="{}'s Skin IDs".format(champ),color=0x6E3582)
        embed.set_thumbnail(url=urls)
        for skins in data['data'][str(champ)]['skins']:
            embed.add_field(name=(str.title(skins['name'])) + ":" ,value="Skin ID: " + str(skins['num']),inline=False)
            client.say(skins)
        await client.say(embed=embed)
    except Exception as e:
        await client.say("Champion Not Found!")
    txt.close()



@client.command(pass_context=True, brief="Use this for league skin splashes tho u need to know skin id, find this using '=skinid (champ)'")
async def skin(ctx, skinid, *, champion):
    original = str.title(champion)
    champion = str.title(champion)
    if champion == "Wukong":
        champion = "MonkeyKing"
    new_champion = champion.replace(' ', '')
    imgurl = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + new_champion + "_{}.jpg".format(skinid)
    q = requests.get(imgurl)
    if str(q) == "<Response [200]>":
        embed = discord.Embed(title=original, description="{}'s Skin Art".format(original), color=0x003366)
        embed.set_image(url=imgurl)
        embed.set_footer(text="League of Legends",
                         icon_url="https://vignette.wikia.nocookie.net/leagueoflegends/images/1/12/League_of_Legends_Icon.png/revision/latest?cb=20150402234343")
        await client.say(embed=embed)
    else:
        await client.say("Something Went Wrong Try Again")
    await client.delete_message(ctx.message)

@client.command(pass_context=True)
@commands.cooldown(1,3,BucketType.server)
async def build(ctx,role,*,id):
    try:

        ogrole=str(role)
        role=str(role)
        role=str.upper(role)
        if role=="BOTTOM":
            role="DUO_CARRY"
        elif role=="SUPPORT":
            role="DUO_SUPPORT"
        elif role=="MID":
            role="MIDDLE"
        elif role=="ADC":
            role="DUO_CARRY"
        elif role=="BOT":
            role="DUO_CARRY"
        id =str(id)
        id=str.title(id)
        namefortitle=id
        name=id.replace(" ","")
        py_gg.init("265960d76589c37fd56831905f6c53a8")
        ses= requests.Session()
        txts=ses.get("http://ddragon.leagueoflegends.com/cdn/8.9.1/data/en_US/champion.json")
        full_ids=txts.text
        data = json.loads(full_ids.encode('utf-8'))
        urls="https://ddragon.leagueoflegends.com/cdn/8.9.1/img/champion/" + str(data['data'][str(name)]['image']['full'])
        d=data['data'][str(name)]['key']
        print(d)
        ses= requests.Session()
        txt=ses.get("http://ddragon.leagueoflegends.com/cdn/8.9.1/data/en_US/item.json")
        ids=txt.text
        dat=json.loads(ids.encode('utf-8'))
        if len(dat) < 1:
            await client.say("2nd limit hit (item data)")
        else:
            data = py_gg.champions.specific_role(int(d), role, options={"champData": "hashes"})
            hwr_items = data["hashes"]["finalitemshashfixed"]["highestCount"]["hash"]
            hwr_items = hwr_items.split("-")[1:]
            a=int(len(hwr_items))
            embed=discord.Embed(title="Highest Playrate Build For {}".format(namefortitle),color=0xFCFB00 )
            for z in range(0,a):
                hwr_items[z]=dat['data'][hwr_items[z]]['name']
            for i in range(0,a):
                embed.add_field(name="Item {}".format(str(i+1)),value=str(hwr_items[i]),inline=False)
            embed.set_thumbnail(url=urls)
            embed.set_footer(text=str.title(ogrole))
            await client.delete_message(ctx.message)
            await client.say(embed=embed)
    except commands.errors.CommandOnCooldown:
        await client.say("Command is on Cooldown 1 Uses Per 3 Second")
    except Exception as e:
        await client.say("Either This Champion Doesnt Belong in This Role or This Champion Doesnt Exist or Rate Limit Hit")




@client.command(pass_context=True)
async def flip(ctx):
    links = ["http://i.dailymail.co.uk/i/pix/2009/11/25/article-1230900-06ACAD44000005DC-544_306x300.jpg",
             "http://i.dailymail.co.uk/i/pix/2009/11/25/article-1230900-06ACACE3000005DC-846_306x300.jpg"]
    em = discord.Embed(title="Coin Flip", color=0xAC00AA)
    em.set_thumbnail(url=random.choice(links))
    await client.send_message(ctx.message.channel, embed=em)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def info(ctx, *, member: discord.Member = None):
    member = member or ctx.message.author
    av = member.avatar_url
    if ".gif" in av:
        av += "&f=.gif"
    join = str(member.joined_at)
    join = join[:len(join) - 7]
    embed = discord.Embed(title="{}'s Info:".format(member.name), description="Here's What I Could Find:",
                          color=0xFF66BE)
    embed.add_field(name="Username:", value=member.name, inline=True)
    embed.add_field(name="ID:", value=member.id, inline=True)
    embed.add_field(name="Status:", value=member.status, inline=True)
    embed.add_field(name="Highest Role:", value=member.top_role, inline=True)
    embed.add_field(name="Joined At:", value=join, inline=True)
    embed.set_thumbnail(url=av)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def insult(ctx):
    result = [" is a korean boy loving ass", " is a lolifurry", " likes boy semen", " likes dem wrickled tits",
              " likes his brothers rod", " IS A DOUCHEBAGGETE", " im jealous of everyone who HASN'T MET YOU",
              " IS A DOGGYKNOBBER", " licks his mothers minge"]
    members = list(ctx.message.server.members)
    person = str(random.choice(members))
    await client.say(person[:len(person) - 5] + random.choice(result))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='With Kevin'))



client.run(TOKEN)
