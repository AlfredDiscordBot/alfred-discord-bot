import traceback
import requests
import nextcord
import utils.assets as assets
import utils.External_functions as ef
import utils.Trend as Trend

from nextcord.ext import commands, tasks
from functools import lru_cache
from utils.Storage_facility import Variables
from dataclasses import dataclass
from .Embed import filter_graves, embed_from_dict
from datetime import datetime
from typing import Any, List, Dict, Union, Optional

# Coded by Shravan-1908
# Use nextcord.slash_command()

CACHE_USER, CACHE_REPO = {}, {}


def requirements():
    return []


class CodeExecutor:
    """
    Base class for code executing utilities.
    """

    def __init__(self) -> None:
        self.runtimes = self.get_runtimes()

    @staticmethod
    def get_runtimes() -> List[Dict[str, Union[str, List[str]]]]:
        """
        Returns a list of all available runtimes in the piston api.
        """
        try:
            runtime_url = "https://emkc.org/api/v2/piston/runtimes"
            data = requests.get(runtime_url, timeout=10).json()
            runtimes: List[Dict[str, Union[str, List[str]]]] = []
            for langs in data:
                runtimes.append(
                    {
                        "language": langs["language"],
                        "version": langs["version"],
                        "aliases": [i for i in langs["aliases"]],
                    }
                )

            return runtimes

        except Exception as e:
            traceback.print_exc(e)

    @lru_cache(maxsize=50)
    def execute_code(self, language: str, code: str) -> str:
        """
        Executes the given code in the given language and version.
        """
        try:
            execute_url = "https://emkc.org/api/v2/piston/execute"
            all_langs = [runtime["language"] for runtime in self.runtimes]
            _aliases = [runtime["aliases"] for runtime in self.runtimes]
            aliases = [i for sublist in _aliases for i in sublist]

            if language not in all_langs and language not in aliases:
                return f"Language {language} is not supported."

            for runtime in self.runtimes:
                if runtime["language"] == language or language in runtime["aliases"]:
                    version = runtime["version"]
                    break

            payload = {
                "language": language,
                "version": version,
                "files": [
                    {
                        "name": "prog",
                        "content": code,
                    }
                ],
            }

            resp = requests.post(execute_url, json=payload)

            if resp.status_code == 200:
                data = resp.json()
                run_data = data["run"]

                return f"""
Exit Code: {run_data["code"]}

Output:
```
{run_data["output"][:500]}
```
                """

            else:
                return f"Error: {resp.status_code}"

        except Exception as e:
            traceback.print_exc(e)
            return "Couldn't connect at the moment."


@dataclass
class GitHubUserStats:
    name: str
    avatar_url: str
    followers: int
    following: int
    public_repos: int
    public_gists: int
    html_url: str
    bio: str
    company: str
    location: str
    email: Optional[str]

    def __repr__(self) -> str:
        result = ""
        result += f"Name: {self.name}\n"
        result += f"Avatar URL: {self.avatar_url}\n"
        result += f"Followers: {self.followers}\n"
        result += f"Following: {self.following}\n"
        result += f"Public Repos: {self.public_repos}\n"
        result += f"Public Gists: {self.public_gists}\n"
        result += f"HTML URL: {self.html_url}\n"
        result += f"Bio: {self.bio}\n"
        result += f"Company: {self.company}\n"
        result += f"Location: {self.location}\n"
        result += f"Email: {self.email}\n"
        return result


@lru_cache(maxsize=20)
def get_user_stats(username: str) -> Union[GitHubUserStats, None]:
    if username not in CACHE_USER:
        r = requests.get(f"https://api.github.com/users/{username}")

        if r.status_code != 200:
            return None

        user_stats: dict = r.json()
        CACHE_USER[username] = user_stats
    else:
        user_stats = CACHE_USER[username]

    return GitHubUserStats(
        name=user_stats["name"],
        avatar_url=user_stats["avatar_url"],
        followers=user_stats["followers"],
        following=user_stats["following"],
        public_repos=user_stats["public_repos"],
        public_gists=user_stats["public_gists"],
        html_url=user_stats["html_url"],
        bio=user_stats["bio"],
        company=user_stats["company"],
        location=user_stats["location"],
        email=user_stats["email"],
    )


@dataclass
class GitHubRepoStats:
    name: str
    owner: str
    description: str
    language: str
    stargazers_count: int
    forks_count: int
    html_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    size: str
    open_issues: int
    watchers: int
    subscribers_count: int
    license: Optional[str]
    topics: List[str]
    homepage: str
    owner_thumbnail: str
    image: str

    def __repr__(self) -> str:
        result = ""
        result += f"Name: {self.name}\n"
        result += f"Owner: {self.owner}\n"
        result += f"Description: {self.description}\n"
        result += f"Language: {self.language}\n"
        result += f"Stargazers Count: {self.stargazers_count}\n"
        result += f"Forks Count: {self.forks_count}\n"
        result += f"HTML URL: {self.html_url}\n"
        result += f"Created At: {self.created_at}\n"
        result += f"Updated At: {self.updated_at}\n"
        result += f"Pushed At: {self.pushed_at}\n"
        result += f"Size: {self.size}\n"
        result += f"Open Issues: {self.open_issues}\n"
        result += f"Watchers: {self.watchers}\n"
        result += f"Subscribers Count: {self.subscribers_count}\n"
        result += f"License: {self.license}\n"
        result += f"Topics: {', '.join(self.topics)}\n"
        result += f"Homepage: {self.homepage}\n"
        return result


@lru_cache(maxsize=50)
def fetch_image(url: str) -> str:
    return f"https://opengraph.githubassets.com/1/{url}"


@lru_cache(maxsize=20)
async def get_repo_stats(repo: str) -> Union[GitHubRepoStats, None]:
    if repo not in CACHE_REPO:
        repo_stats = await ef.get_async(
            f"https://api.github.com/repos/{repo}",
            headers={"Accept": "application/vnd.github.mercy-preview+json"},
            kind="json",
        )
        CACHE_REPO[repo] = repo_stats
    else:
        repo_stats = CACHE_REPO[repo]
    image = fetch_image(repo)

    if repo_stats.get("message"):
        return None

    if not repo_stats.get("license", None):
        repo_stats["license"] = ""
    else:
        repo_stats["license"] = repo_stats["license"]["name"]

    return GitHubRepoStats(
        name=repo_stats.get("name", ""),
        description=repo_stats.get("description", ""),
        language=repo_stats.get("language", ""),
        stargazers_count=repo_stats.get("stargazers_count", ""),
        forks_count=repo_stats.get("forks_count", ""),
        html_url=repo_stats.get("html_url", ""),
        created_at=repo_stats.get("created_at", ""),
        updated_at=repo_stats.get("updated_at", ""),
        pushed_at=repo_stats.get("pushed_at", ""),
        size=f"{int(repo_stats.get('size', 0)) / 1000:.2f} MBs",
        open_issues=repo_stats.get("open_issues", ""),
        watchers=repo_stats.get("watchers", ""),
        subscribers_count=repo_stats.get("subscribers_count", ""),
        license=repo_stats.get("license", ""),
        topics=repo_stats.get("topics", ""),
        homepage=repo_stats.get("homepage", ""),
        owner=repo_stats.get("owner", {}).get("login"),
        owner_thumbnail=repo_stats.get("owner", {}).get("avatar_url", None),
        image=image,
    )


async def repo_stats_dict(stats: GitHubRepoStats, color: int = None):
    info = {}
    info["title"] = f"{stats.owner}/{stats.name}"
    info["description"] = f"{stats.description if stats.description else ''}"

    if homepage := stats.homepage:
        info["description"] = info["description"] + "Homepage: " + homepage + "\n"

    if color:
        color = str(nextcord.Color(color).to_rgb())
        info["color"] = color

    info["url"] = stats.html_url
    info["author"] = {"name": stats.owner, "icon_url": stats.owner_thumbnail}
    if stats.image:
        info["image"] = stats.image
    info[
        "thumbnail"
    ] = "https://www.nicepng.com/png/full/52-520535_free-files-github-github-icon-png-white.png"
    info["fields"] = [
        {
            "name": "Stats",
            "value": f"💻` Language:` {stats.language} \n🍴` Forks:` {stats.forks_count} \n⭐` Stars:` {stats.stargazers_count} \n📰` License:` {stats.license}",
            "inline": False,
        },
        {
            "name": "People",
            "value": f"👀` Watchers:` {stats.watchers} \n⁉️` Issues:` {stats.open_issues} \n👍` Subscribers:` {stats.stargazers_count}",
            "inline": False,
        },
        {
            "name": "Topics",
            "value": "```\n#️⃣"
            + ("\n#️⃣".join(stats.topics) if len(stats.topics) > 0 else "No topics")
            + "\n```",
            "inline": False,
        },
        {
            "name": "Dates",
            "value": f"⌚` Created:` {ef.iso2dtime(stats.created_at)} \n⌚` Updated:` {ef.iso2dtime(stats.created_at)} \n⌚` Pushed:` {ef.iso2dtime(stats.pushed_at)}",
            "inline": False,
        },
    ]
    info["footer"] = f"Owner: {stats.owner}"

    if color:
        info["color"] = color

    return info


def user_stats_dict(stats: GitHubUserStats, color: int = None, uname: str = ""):
    info = {}
    if color:
        color = str(nextcord.Color(color).to_rgb())
        info["color"] = color

    info["title"] = stats.name or uname
    info["thumbnail"] = stats.avatar_url
    info["url"] = stats.html_url
    info["author"] = {"name": stats.name, "icon_url": stats.avatar_url}
    info["image"] = stats.avatar_url

    info[
        "description"
    ] = f"```{stats.bio or ' '}``` \n{stats.name} has {stats.public_repos} public repos and {stats.public_gists} public gists"

    info["fields"] = [
        {
            "name": "More",
            "value": f"```yml\nFollowers: {stats.followers} \nFollowing: {stats.following} \nCompany: {stats.company or ' '} \nLocation: {stats.location or ' '}\n```",
        }
    ]

    return info


class GhCacheControl:
    def __init__(self):
        self.repository: list = []
        self.SETUP: bool = False

    def github_cache(self, load: bool = True, **kwargs):
        if load:
            v = Variables("cogs/__pycache__/ghcache")
            d = v.show_data()
            return d.get("repo", []), d.get("time", 0)
        else:
            v = Variables("cogs/__pycache__/ghcache")
            v.pass_all(**kwargs, time=int(ef.time.time()))
            v.save()
            d = v.show_data()
            return d.get("repo", []), d.get("time", 0)

    def add_pages(self, l: list, t: int) -> list:
        new_embeds = []
        count = 0
        for i in l:
            count += 1
            i["footer"] = {
                "text": f"{count} of {len(l)}",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/25/25231.png",
            }
            new_embeds.append(i)
        return new_embeds

    async def setup(self):
        r, t = self.github_cache(load=True)
        if int(ef.time.time()) - t > 86400:
            print("Updating GhCache")
            trending = await Trend.fetch_trending()
            self.repository = self.add_pages([i.return_dict() for i in trending], t)
            self.github_cache(load=False, repo=self.repository)
        else:
            self.repository = r
        self.SETUP = True

    async def refresh(self):
        await self.setup()

    def trending_repositories(self):
        return [ef.cembed(**i) for i in self.repository]


class Code(
    commands.Cog,
    description="Has tons of stuff that could help you code```\n✅Runs Basic code in EMKC\n✅Github Repository and users\n✅JSON VIEWER\n```",
):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT
        self.rce = CodeExecutor()
        self.ghtrend = GhCacheControl()
        self.CACHE_USER_REPO = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.ghtrend.setup()
        await self.update_loop.start()

    @tasks.loop(hours=4)
    async def update_loop(self):
        await self.ghtrend.refresh()

    def runtimes_to_str(self, runtime: dict) -> str:
        return f"+ {runtime['language']} -> {runtime['version']}"

    async def get_repos(self, username: str, inter: nextcord.Interaction):
        if username not in self.CACHE_USER_REPO:
            j = await ef.get_async(
                f"https://api.github.com/users/{username}/repos", kind="json"
            )
            self.CACHE_USER_REPO[username] = j
        else:
            j = self.CACHE_USER_REPO[username]
        repo_embeds = []
        for repo_stats in j:
            image = fetch_image(repo_stats.get("full_name"))
            if not repo_stats.get("license", None):
                repo_stats["license"] = {}
            else:
                repo_stats["license"] = repo_stats["license"]["name"]
            repo = GitHubRepoStats(
                name=repo_stats.get("name", ""),
                description=repo_stats.get("description", ""),
                language=repo_stats.get("language", ""),
                stargazers_count=repo_stats.get("stargazers_count", ""),
                forks_count=repo_stats.get("forks_count", ""),
                html_url=repo_stats.get("html_url", ""),
                created_at=repo_stats.get("created_at", ""),
                updated_at=repo_stats.get("updated_at", ""),
                pushed_at=repo_stats.get("pushed_at", ""),
                size=f"{int(repo_stats.get('size', 0)) / 1000:.2f} MBs",
                open_issues=repo_stats.get("open_issues", ""),
                watchers=repo_stats.get("watchers", ""),
                subscribers_count=repo_stats.get("subscribers_count", ""),
                license=repo_stats.get("license", ""),
                topics=repo_stats.get("topics", ""),
                homepage=repo_stats.get("homepage", ""),
                owner=repo_stats.get("owner", "").get("login", ""),
                owner_thumbnail=repo_stats.get("owner", {}).get("avatar_url", None),
                image=image,
            )
            info = await repo_stats_dict(repo, self.CLIENT.color(inter.guild))
            repo_embeds.append(embed_from_dict(info, inter, self.CLIENT))
        return repo_embeds

    @commands.command(name="code", aliases=["run"], description="Run Code through EMKC")
    @commands.check(ef.check_command)
    async def code_prefix(self, ctx, lang: str = None, *, code: str = None):
        if not lang or not code:
            runtimes = "\n".join([self.runtimes_to_str(i) for i in self.rce.runtimes])

            embed = ef.cembed(
                title="RunTimes",
                description=f"```diff\nHere are all the languages supported by EMKC\n\n{runtimes}\n```",
                color=self.CLIENT.color(ctx.guild),
                thumbnail=self.CLIENT.user.avatar.url,
                author=self.CLIENT.user,
                footer="**Code and Language are a required argument",
            )
            await ctx.send(embed=embed)
            return

        actual_code = filter_graves(code)
        output = self.rce.execute_code(language=lang, code=actual_code)

        await ctx.reply(
            embed=ef.cembed(
                title="Output",
                description=output,
                color=self.CLIENT.color(ctx.guild),
                thumbnail=self.CLIENT.user.avatar.url,
                author=ctx.author,
                url=ctx.message.jump_url,
                footer={
                    "text": "This result was provided by EMKC",
                    "icon_url": "https://emkc.org/images/icon_square_64.png",
                },
            )
        )

    @commands.command()
    @commands.check(ef.check_command)
    async def json_viewer(self, ctx, url: str):
        await assets.test_JSON(ctx, url=url)

    @nextcord.slash_command(
        name="code", description="This is a paradise for developers"
    )
    async def code(self, inter):
        print(inter.user)

    @code.subcommand(name="github", description="Get info about Github...")
    async def gh(self, inter):
        print(inter.user)

    @code.subcommand(name="json", description="View Json file from here")
    async def json_v_slash(self, inter, url: str):
        await inter.response.defer()
        await assets.test_JSON(inter, url)

    @gh.subcommand(description="User")
    async def user(self, inter, user: str):
        if not inter.message:
            await inter.response.defer()
        stats = get_user_stats(user)
        if stats:
            stats_dict = user_stats_dict(stats, self.CLIENT.color(inter.guild), user)
            stats_dict["footer"] = {
                "text": inter.user.name,
                "icon_url": inter.user.avatar,
            }
            repos = await self.get_repos(user, inter)
        else:
            stats_dict = {
                "title": "UserNotFound",
                "description": "Sorry we couldn't find this user",
                "author": {
                    "name": inter.user.name,
                    "icon_url": ef.safe_pfp(inter.user),
                },
            }
            repos = []
        embed = embed_from_dict(stats_dict, inter, self.CLIENT)
        await assets.pa(inter, [embed] + repos, restricted=True)

    @gh.subcommand(description="Repository")
    async def repo(self, inter, repo: str):
        stats = await get_repo_stats(repo)

        if stats:
            stats_embed = await repo_stats_dict(stats, self.CLIENT.color(inter.guild))
        else:
            stats_embed = {
                "title": "Repository Not Found",
                "description": "I'm sorry, I couldn't find that repository",
                "author": {
                    "name": inter.user.name,
                    "icon_url": ef.safe_pfp(inter.user),
                },
                "color": self.CLIENT.color(inter.guild),
            }
        embed = embed_from_dict(stats_embed, inter, self.CLIENT)
        await inter.send(embed=embed)

    @gh.subcommand(name="trending", description="Gives a list of trending repositories")
    async def trending_repo(self, inter):
        await inter.response.defer()
        await self.ghtrend.setup()
        await assets.pa(inter, self.ghtrend.trending_repositories(), t="sb")

    @code.subcommand(name="pypi", description="Get a package from PyPi")
    async def pypi_slash(self, inter, package: str = "nextcord"):
        await inter.response.defer()
        embeds = await ef.pypi_call(package=package, ctx=inter)
        await assets.pa(inter, embeds, t="s")


def setup(CLIENT, **i):
    CLIENT.add_cog(Code(CLIENT, **i))
