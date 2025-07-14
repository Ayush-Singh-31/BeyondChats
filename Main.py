#!/usr/bin/env python3

import argparse
import os
import sys
from typing import List, Dict

import praw
import openai

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output")
    return parser.parse_args()

def extract_username(url: str) -> str:
    parts = url.rstrip("/").split("/")
    if "user" in parts:
        idx = parts.index("user")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    raise ValueError(f"Could not extract username from URL: {url}")

def init_reddit() -> praw.Reddit:
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "reddit-persona-script/0.1")
    if not client_id or not client_secret:
        print("Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables.", file=sys.stderr)
        sys.exit(1)
    return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

def fetch_user_content(reddit: praw.Reddit, username: str, limit: int) -> List[Dict[str, str]]:
    user = reddit.redditor(username)
    content: List[Dict[str, str]] = []
    for comment in user.comments.new(limit=limit):
        content.append({"type": "comment", "text": comment.body, "url": f"https://www.reddit.com{comment.permalink}"})
    for submission in user.submissions.new(limit=limit):
        body = submission.selftext or ""
        url = submission.url if submission.url.startswith("http") else f"https://www.reddit.com{submission.permalink}"
        content.append({"type": "post", "text": f"{submission.title}\n\n{body}", "url": url})
    return content

def generate_persona(content: List[Dict[str, str]], username: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        print("Please set OPENAI_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)
    chunks = [f"URL: {item['url']}\nType: {item['type']}\nContent:\n{item['text']}" for item in content]
    prompt = (
        f"Given the following Reddit content from user u/{username}, "
        "build a concise user persona. For each characteristic, cite the specific URL from which it was derived.\n\n"
        f"{'\n\n'.join(chunks)}\n\nPersona:\n"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

def save_persona(persona: str, output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(persona)
    print(f"Persona saved to {output_file}")

def main() -> None:
    args = parse_args()
    try:
        username = extract_username(args.url)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    reddit = init_reddit()
    content = fetch_user_content(reddit, username, args.limit)
    if not content:
        print(f"No content found for user {username}", file=sys.stderr)
        sys.exit(1)
    persona = generate_persona(content, username)
    output_file = args.output or f"{username}_persona.txt"
    save_persona(persona, output_file)

if __name__ == "__main__":
    main()
