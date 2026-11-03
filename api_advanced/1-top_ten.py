#!/usr/bin/python3
"""Query the Reddit API and print the first 10 hot posts."""

import os
import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts."""
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")

    if not client_id or not client_secret or not subreddit:
        print(None)
        return

    headers = {
        "User-Agent": "ALUStudent:top_ten:v1.0"
    }

    token_url = "https://www.reddit.com/api/v1/access_token"

    try:
        token_response = requests.post(
            token_url,
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials"},
            headers=headers,
            allow_redirects=False,
            timeout=10
        )

        if token_response.status_code != 200:
            print(None)
            return

        access_token = token_response.json().get("access_token")

        if not access_token:
            print(None)
            return

        headers["Authorization"] = "Bearer {}".format(access_token)

        url = "https://oauth.reddit.com/r/{}/hot".format(subreddit)

        response = requests.get(
            url,
            headers=headers,
            params={"limit": 10},
            allow_redirects=False,
            timeout=10
        )

        if response.status_code != 200:
            print(None)
            return

        posts = response.json().get("data", {}).get("children", [])

        for post in posts[:10]:
            print(post.get("data", {}).get("title"))

    except (requests.RequestException, ValueError):
        print(None)

