from typing import List, Union
import requests
from dataclasses import dataclass


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
    email: str

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
    size: int
    open_issues: int
    watchers: int
    subscribers_count: int
    license: str
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


def get_repo_stats(repo: str) -> Union[GitHubRepoStats, None]:
    r = requests.get(f"https://api.github.com/repos/{repo}", headers={"Accept": "application/vnd.github.mercy-preview+json"})

    if r.status_code != 200:
        return None

    repo_stats: dict = r.json()
    return GitHubRepoStats(
        name=repo_stats["name"],
        description=repo_stats["description"],
        language=repo_stats["language"],
        stargazers_count=repo_stats["stargazers_count"],
        forks_count=repo_stats["forks_count"],
        html_url=repo_stats["html_url"],
        created_at=repo_stats["created_at"],
        updated_at=repo_stats["updated_at"],
        pushed_at=repo_stats["pushed_at"],
        size=repo_stats["size"],
        open_issues=repo_stats["open_issues"],
        watchers=repo_stats["watchers"],
        subscribers_count=repo_stats["subscribers_count"],
        license=repo_stats["license"]["name"],
        topics=repo_stats["topics"],
        homepage=repo_stats["homepage"],
        owner=repo_stats["owner"]["login"],
    )


def requirements():
    return ["re"]

def main(client, re):
    pass

if __name__ == "__main__":
    r1 = (str(get_user_stats("Shravan-1908")))
    r2 = (str(get_repo_stats("Shravan-1908/iris")))
    print(r1)
    print(r2)