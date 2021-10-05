import sys

sys.path.append("./src")

from github_stats import *


def test_github_user_stats():
    resp = get_user_stats("Shravan-1908")
    assert resp is not None

    invalid_user = get_user_stats("Shravan-1908/hydra")
    assert invalid_user is None


def test_github_repo_stats():
    resp = get_repo_stats("Shravan-1908/hydra")
    assert resp is not None

    invalid_repo = get_repo_stats("Shravan-1908")
    assert invalid_repo is None
