import nextcord
import utils.External_functions as ef

BeautifulSoup = ef.BeautifulSoup


async def fetch_trending():
    html = await ef.get_async("https://github.com/trending")
    soup = BeautifulSoup(html, "lxml")
    box = (
        soup.find("div", class_="application-main")
        .main.find("div", class_="position-relative container-lg p-responsive pt-6")
        .div
    )
    repositories = box.find_all("article")
    return [TrendDictGen(i) for i in repositories]


class TrendDictGen:
    def __init__(self, soup: BeautifulSoup):
        self.SOUP = soup
        self.misc_data = self.SOUP.find("div", class_="f6 color-fg-muted mt-2")
        self.di = {
            "title": self.title(),
            "url": self.url(),
            "description": self.description(),
            "fields": {},
            "thumbnail": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
            "image": f"https://opengraph.githubassets.com/1{self.SOUP.h1.a['href']}",
        }
        self.url()
        self.process_misc_data()

    def return_dict(self):
        return self.di

    def title(self):
        title = self.SOUP.h1.get_text().strip()
        return "/".join([i.strip() for i in title.split("/")])

    def url(self):
        return "https://github.com/" + self.SOUP.h1.a["href"]

    def description(self):
        return "```\n" + self.SOUP.p.get_text().strip() + "\n```" if self.SOUP.p else ""

    def process_misc_data(self):
        lang = self.misc_data.find("span", class_="d-inline-block ml-0 mr-3")
        if lang:
            lang_color = lang.find("span", class_="repo-language-color")[
                "style"
            ].split()[-1]
            self.di["color"] = nextcord.Color.from_rgb(*ef.extract_color(lang_color))
            self.di["fields"].update(
                {"Stats": f"`Language: ` {lang.get_text().strip()}\n"}
            )
        for i in self.misc_data.find_all("a"):
            if "Stats" not in self.di["fields"]:
                self.di["fields"] = {"Stats": ""}
            if "/stargazers" in i["href"]:
                self.di["fields"]["Stats"] += f"`Stars: `{i.get_text().strip()}🌟\n"
            elif "/network/members." in i["href"]:
                self.di["fields"]["Stats"] += f"`Forks: `{i.get_text().strip()}🍴"

        de = self.misc_data.find("span", class_="d-inline-block mr-3")
        developers = []
        if de:
            main_author = de.find_all("a")[0]
            self.di["author"] = {
                "name": main_author["href"][1:],
                "url": "https://github.com" + main_author["href"],
                "icon_url": main_author.img["src"],
            }
            for i in de.find_all("a"):
                u = i["href"][1:]
                developers.append(f"[{u}](https://github.com/{u})")
            self.di["fields"]["Developers🧑‍💻"] = "\n".join(developers)
