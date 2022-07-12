import traceback
import requests
import nextcord
import utils.External_functions as ef

from nextcord.ext import commands
from functools import lru_cache
from dataclasses import dataclass
from .Embed import filter_graves, embed_from_dict
from typing import (
    List,
    Dict,
    Union,
    Optional
)

# Coded by Shravan-1908
# Use nextcord.slash_command()

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
    r = requests.get(f"https://api.github.com/users/{username}")

    if r.status_code != 200:
        return None

    user_stats: dict = r.json()

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


@lru_cache(maxsize=20)
def get_repo_stats(repo: str) -> Union[GitHubRepoStats, None]:
    r = requests.get(
        f"https://api.github.com/repos/{repo}",
        headers={"Accept": "application/vnd.github.mercy-preview+json"},
    )

    if r.status_code != 200:
        return None

    repo_stats: dict = r.json()

    if not repo_stats:
        return None

    if not repo_stats.get("license", None):
        repo_stats["license"] = {}

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
        license=repo_stats["license"].get("name", ""),
        topics=repo_stats.get("topics", ""),
        homepage=repo_stats.get("homepage", ""),
        owner=repo_stats.get("owner", "").get("login", ""),
    )


def repo_stats_dict(stats: GitHubRepoStats, color: int = None):
    info = {}
    info["title"] = f"{stats.owner}/{stats.name}"
    info["description"] = f"{stats.description} \nLicense: {stats.license} \n"

    if homepage := stats.homepage:
        info["description"] = info["description"] + "Homepage: " + homepage + "\n"

    if color:
        color = str(nextcord.Color(color).to_rgb())
        info["color"] = color

    info["url"] = stats.html_url
    info[
        "thumbnail"
    ] = "https://www.nicepng.com/png/full/52-520535_free-files-github-github-icon-png-white.png"
    info["fields"] = [
        {
            "name": "Stats",
            "value": f"lang: {stats.language} \nForks: {stats.forks_count} \nStars: {stats.stargazers_count}",
        },
        {
            "name": "Stats",
            "value": f"Watchers: {stats.watchers} \nIssues: {stats.open_issues} \nSubscribers: {stats.stargazers_count}",
        },
        {
            "name": "Topics",
            "value": ", ".join(stats.topics) if len(stats.topics)>0 else "No topics",
        },
        {
            "name": "Dates",
            "value": f"Created: {stats.created_at} \nUpdated: {stats.created_at} \nPushed: {stats.pushed_at}",
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

    info[
        "description"
    ] = f"```{stats.bio or ' '}``` \n{stats.name} has {stats.public_repos} public repos and {stats.public_gists} public gists"

    info["fields"] = [
        {
            "name": "More",
            "value": f"Followers: {stats.followers} \nFollowing: {stats.following} \nCompany: {stats.company or ' '} \nLocation: {stats.location or ' '}",
        }
    ]

    if email := stats.email:
        info["footer"] = f"email: {email}"

    return info


class Code(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rce = CodeExecutor()

    def runtimes_to_str(self, runtime: dict) -> str:
        return f"+ {runtime['language']} -> {runtime['version']}"

    @commands.command(
        name="code",
        aliases=['run'],
        description="Run Code through EMKC"
    )
    async def code(self, ctx, lang: str = None, *, code: str = None):
        if not lang or not code:
            runtimes = "\n".join([
                self.runtimes_to_str(i) for i in self.rce.runtimes
            ])         

            
            embed=ef.cembed(
                title="RunTimes",
                description=f"```diff\nHere are all the languages supported by EMKC\n\n{runtimes}\n```",
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url,
                author=self.client.user,
                footer="**Code and Language are a required argument"
            )
            await ctx.send(
                embed=embed
            )
            return    

        actual_code = filter_graves(code)
        output = self.rce.execute_code(language=lang, code=actual_code)

        await ctx.reply(
            embed=ef.cembed(
                title="Output",
                description=output,
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url,
                author=ctx.author,
                footer={
                    'text': 'This result was provided by EMKC',
                    'icon_url': 'https://emkc.org/images/icon_square_64.png'
                }
            )
        )
    
    @nextcord.slash_command(name="github", description="Get info about Github...")
    async def gh(self, inter):
        print(inter.user)

    @gh.subcommand(description="User")
    async def user(self, inter, user: str): 
        await inter.response.defer()
        stats = get_user_stats(user)
        if stats:
            stats_dict = user_stats_dict(stats, self.client.re[8], user)
        else:
            stats_dict = {
                'title':'UserNotFound',
                'description':'Sorry we couldn\'t find this user',
                'author':{
                    'name': inter.user.name,
                    'icon_url': ef.safe_pfp(inter.user)
                }
            }
        embed = embed_from_dict(
            stats_dict, inter, self.client
        )
        await inter.send(embed=embed)

    @gh.subcommand(description="Repository")
    async def repo(self, inter, repo: str):
        stats = get_repo_stats(repo)

        if stats:
            stats_embed = repo_stats_dict(
                stats, self.client.re[8]
            )
        else:
            stats_embed = {
                'title': 'Repository Not Found',
                'description': 'I\'m sorry, I couldn\'t find that repository',
                'author': {
                    'name': inter.user.name,
                    'icon_url': ef.safe_pfp(inter.user)
                },
                'color': self.client.re[8]
            }
        embed=embed_from_dict(
            stats_embed, inter, self.client
        )
        await inter.send(embed=embed)


def setup(client,**i):
    client.add_cog(Code(client,**i))