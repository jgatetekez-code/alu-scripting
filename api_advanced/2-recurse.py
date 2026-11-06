#!/usr/bin/python3
"""Module that recursively retrieves hot Reddit posts."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return titles of all hot posts in a subreddit."""
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": "ALUStudent:reddit_api:v1.0"
    }

    params = {"limit": 100}

    if after:
        params["after"] = after

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )

        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        posts = data.get("children", [])

        for post in posts:
            title = post.get("data", {}).get("title")
            if title is not None:
                hot_list.append(title)

        next_after = data.get("after")

        if next_after:
            return recurse(subreddit, hot_list, next_after)

        return hot_list if hot_list else None

    except (requests.RequestException, ValueError):
        return None

