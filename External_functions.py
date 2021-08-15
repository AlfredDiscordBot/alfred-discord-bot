import requests
import requests
import hashlib
import psutil
import os
import discord
import imdb
from dotenv import load_dotenv
from instagramy import *
from instascrape import *


def quad(eq):
    if "x^2" not in eq:
        return "x^2 not found, try again"
    print(eq)
    eq = eq.replace("2+", "2 + ")
    eq = eq.replace("2-", "2 - ")
    eq = eq.replace("x+", "x + ")
    eq = eq.replace("x-", "x - ")

    # try to get correct equation
    parts = [x.strip() for x in eq.split(" ")]
    a, b, c = 0, 0, 0
    for i in parts:
        if i == ' ':
            parts.remove(' ')

    for index, part in enumerate(parts):
        if part in ["+", "-"]:
            continue

        symbol = -1 if index - 1 >= 0 and parts[index - 1] == "-" else 1

        if part.endswith("x^2"):
            coeff = part[:-3]
            a = float(coeff) if coeff != '' else 1
            a *= symbol
        elif part.endswith("x"):
            coeff = part[:-1]
            b = float(coeff) if coeff != '' else 1
            b *= symbol
        elif part.isdigit():
            c = symbol * float(part)

    determinant = b**2 - (4 * a * c)

    if determinant < 0:
        return "Not Real"
    if determinant == 0:
        root = -b / (2 * a)
        return "Equation has one root:"+str(root)

    if determinant > 0:
        determinant = determinant ** 0.5
        root1 = (-b + determinant) / (2 * a)
        root2 = (-b - determinant) / (2 * a)
        return "This equation has two roots: "+str(root1)+","+str(root2)


def memes2():
    st = requests.get(
        "https://cheezburger.com/14858757/40-dumb-memes-for-distractible-scrollers").content.decode()
    stop = 0
    link = []
    for i in range(0, 40):
        a = st.find("<img class='resp-media' src='", stop) + \
            len("<img class='resp-media' src='")
        b = st.find("' id", a)
        stop = b
        link = link+[st[a:b]]
    return link


def memes1():
    st = requests.get("http://www.quickmeme.com/").content.decode()
    stop = 0
    link = []
    for i in range(10):
        a = st.find('"post-image" src="', stop)+len('post-image" src="')+1
        b = st.find('" alt', a)
        stop = b
        link = link+[st[a:b]]
    return link


def memes3():
    st = requests.get(
        "https://www.paulbarrs.com/business/funny-memes-website-design").content.decode()
    stop = 0
    link = []
    for i in range(20):
        a = st.find('srcset="', stop)+len('srcset="')
        b = st.find(".jpg", a)+len(".jpg")
        print(st[a:b])
        stop = b
        link += [st[a:b]]
    return link


load_dotenv()


username = str(os.getenv('username'))
password = str(os.getenv('password'))


def get_sessionid(username, password):
    url = "https://i.instagram.com/api/v1/accounts/login/"

    def generate_device_id(username, password):
        m = hashlib.md5()
        m.update(username.encode() + password.encode())

        seed = m.hexdigest()
        volatile_seed = "12345"

        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    device_id = generate_device_id(username, password)

    payload = {
        'username': username,
        'device_id': device_id,
        'password': password,
    }

    headers = {
        'Accept': '*/*',
        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'en-US',
        'referer': "https://www.instagram.com/accounts/login/",
        'User-Agent': "Instagram 10.26.0 Android"
    }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.cookies.get_dict()['sessionid']

    return response.text


def get_it():
    return get_sessionid(username, password)


def instagram_get(account, color, SESSIONID):
    try:
        user = InstagramUser(account, sessionid=SESSIONID)
        url = user.posts[0].post_url
        if True:
            pos = Post(url)
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
                "cookie": "sessionid="+SESSIONID+";"}
            pos.scrape(headers=headers)
            descript = pos.caption
            thumb = user.profile_picture_url
            embed = discord.Embed(
                title="Insta", description=descript, color=discord.Color(value=color))
            embed.set_image(url=user.posts[0].post_source)
            embed.set_thumbnail(url=thumb)
            return (embed, url)

    except Exception as e:
        print(e)
        SESSIONID = get_it()
        return SESSIONID


def get_youtube_url(url):

    '''
    gets the list of url from a channel url
    '''
    st=requests.get(url).content.decode()
    stop=0
    li=[]

    st = requests.get(url).content.decode()
    stop = 0
    li = []

    for i in range(10):
        a = st.find("/watch?v", stop)
        b = st.find('"', a)
        li = li+["https://www.youtube.com"+st[a:b]]
        stop = b
    return li



def cembed(title="",description="",thumbnail="",picture="",color=discord.Color.dark_theme()):
    '''
    A simpler way for creating an embed
    '''
    embed=discord.Embed()
    if color!=discord.Color.dark_theme():
        embed=discord.Embed(color=discord.Color(value=color))
    if title!="":
        embed.title=title
    if description!="":
        embed.description=description
    if thumbnail!="":
        embed.set_thumbnail(url=thumbnail)
    if picture!="":
        embed.set_image(url=picture)            
    return embed

def get_if_process_exists(name):
    return len([i for i in [p.info['name'] for p in psutil.process_iter(['name'])] if i.find(name) != -1]) > 0


def cembed(title="", description="", thumbnail="", picture="", color=discord.Color.dark_theme()):
    embed = discord.Embed()
    if color != discord.Color.dark_theme():
        embed = discord.Embed(color=discord.Color(value=color))
    if title != "":
        embed.title = title
    if description != "":
        embed.description = description
    if thumbnail != "":
        embed.set_thumbnail(url=thumbnail)
    if picture != "":
        embed.set_image(url=picture)
    return embed


def imdb_embed(movie):
    '''
    Returns details about a movie as an embed in discord
    Parameters include movies
    '''
    if movie=="":
        return cembed(title="Oops", description="You must enter a movie name",color=discord.Color.from_rgb(255,255,255).value)
    try:
        ia=imdb.IMDb()
        movie=ia.search_movie(movie)
        title=movie[0]['title']
        summary=ia.get_movie(movie[0].getID()).summary()
        image=movie[0]['full-size cover url']
        return cembed(title=title, description=summary[summary.find("=")+5:],color=discord.Color.from_rgb(255,255,255).value,picture=image)
    except:
        return cembed(title="Oops", description="Something went wrong, check if the name is correct",color=discord.Color.from_rgb(255,255,255).value)
    
    

