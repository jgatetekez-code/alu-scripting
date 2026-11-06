#!/usr/bin/python3
"""Module that queries the Reddit API for a subreddit's hot posts."""
import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts of a subreddit.

    Prints None if the subreddit is invalid.
    """
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:top_ten:v1.0.0 (by /u/your_username)"}
    params = {"limit": 10}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code != 200:
            print(None)
            return
        posts = response.json().get("data", {}).get("children", [])
    except (requests.RequestException, ValueError):
        print(None)
        return

    for post in posts:
        print(post.get("data", {}).get("title"))
