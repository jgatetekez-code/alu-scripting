#!/usr/bin/python3
"""Query the Reddit API for subreddit subscriber counts."""

import os
import requests

def number_of_subscribers(subreddit):
    """Return the total number of subscribers for a subreddit."""
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")

    if not client_id or not client_secret or not subreddit:
        return 0

    headers = {
        "User-Agent": "ALUStudentSubscriberChecker/1.0"
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
            return 0

        access_token = token_response.json().get("access_token")

        if not access_token:
            return 0

        headers["Authorization"] = "Bearer {}".format(access_token)

        url = "https://oauth.reddit.com/r/{}/about".format(subreddit)

        response = requests.get(
            url,
            headers=headers,
            allow_redirects=False,
            timeout=10
        )

        if response.status_code != 200:
            return 0

        data = response.json()
        return data.get("data", {}).get("subscribers", 0)

    except (requests.RequestException, ValueError):
        return 0

