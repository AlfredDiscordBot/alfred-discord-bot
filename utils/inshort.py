# Coded by Sumanjay on 29th Feb 2020
# Made Async by alvinbengeorge on 1st June 2022

from utils.External_functions import get_async, convert_to_url
from bs4 import BeautifulSoup
import re as regex
import requests


async def getNews(category):
    category = convert_to_url(category)
    newsDictionary = {"success": True, "category": category, "data": []}

    try:
        if category != "all":
            htmlBody = await get_async("https://www.inshorts.com/en/read/" + category)
        else:
            htmlBody = await get_async("https://www.inshorts.com/en/read/")

    except Exception as e:
        newsDictionary["success"] = False
        newsDictionary["error"] = str(e.message)
        return newsDictionary

    soup = BeautifulSoup(htmlBody, "lxml")
    newsCards = soup.find_all(class_="news-card")
    if not newsCards:
        newsDictionary["success"] = False
        newsDictionary["error"] = "Invalid Category"
        return newsDictionary

    for index, card in enumerate(newsCards):
        try:
            title = card.find(class_="news-card-title").find("a").text.strip()
        except AttributeError:
            title = None

        try:
            imageUrl = card.find(class_="news-card-image")["style"].split("'")[1]
        except AttributeError:
            imageUrl = None

        try:
            url = "https://www.inshorts.com" + card.find(class_="news-card-title").find(
                "a"
            ).get("href")
        except AttributeError:
            url = None

        try:
            content = card.find(class_="news-card-content").find("div").text
        except AttributeError:
            content = None

        try:
            author = card.find(class_="author").text
        except AttributeError:
            author = None

        try:
            date = card.find(clas="date").text
        except AttributeError:
            date = None

        try:
            time = card.find(class_="time").text
        except AttributeError:
            time = None

        try:
            readMoreUrl = card.find(class_="read-more").find("a").get("href")
        except AttributeError:
            readMoreUrl = None

        newsObject = {
            "title": title,
            "imageUrl": imageUrl,
            "url": url,
            "content": content,
            "author": author,
            "date": date,
            "time": time,
            "readMoreUrl": readMoreUrl,
        }

        newsDictionary["data"].append(newsObject)

    return newsDictionary


def get_categories():
    a = requests.get("https://www.inshorts.com/en/read/").content.decode()
    return [i.split("/")[-1] for i in regex.findall(r"en/read/\w+", a)]
