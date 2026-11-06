#!/usr/bin/python3
"""Module that counts keywords in Reddit hot articles."""
import requests


def count_words(subreddit, word_list, after=None, counts=None,
                multipliers=None, total=0):
    """Recursively count keywords in all hot articles."""
    if counts is None:
        counts = {}
        multipliers = {}

        for word in word_list:
            word = word.lower()
            multipliers[word] = multipliers.get(word, 0) + 1
            counts[word] = 0

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "ALUStudent:RedditAPI:v1.0"}

    params = {"limit": 100, "count": total}

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
            return

        data = response.json().get("data", {})
        posts = data.get("children", [])

        for post in posts:
            title = post.get("data", {}).get("title", "")
            words = title.lower().split()

            for word in words:
                if word in multipliers:
                    counts[word] += multipliers[word]

        after = data.get("after")
        total += len(posts)

        if after:
            return count_words(
                subreddit, word_list, after, counts,
                multipliers, total
            )

        results = sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0])
        )

        for word, count in results:
            if count > 0:
                print("{}: {}".format(word, count))

    except (requests.RequestException, ValueError):
        return

