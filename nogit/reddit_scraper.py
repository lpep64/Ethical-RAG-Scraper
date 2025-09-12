import os
import json
import time
import logging
from dotenv import load_dotenv
import praw
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
SUBREDDITS = os.getenv('SUBREDDITS', '').split(',')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)

def load_checkpoints(checkpoint_file):
    if not os.path.exists(checkpoint_file):
        return set()
    with open(checkpoint_file, 'r') as f:
        return set(line.strip() for line in f)

def save_checkpoint(submission_id, checkpoint_file):
    with open(checkpoint_file, 'a') as f:
        f.write(f"{submission_id}\n")

import re
def clean_text(text):
    # Remove URLs, emojis, extra whitespace, and HTML entities
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)  # Remove emojis
    text = text.replace('&amp;', '&')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_submission(submission):
    data = {
        "id": submission.id,
        "type": "submission",
        "permalink": f"https://www.reddit.com{submission.permalink}",
        "author": str(submission.author),
        "created_utc": int(submission.created_utc),
        "score": submission.score,
        "title": clean_text(submission.title),
        "content": clean_text(submission.selftext)
    }
    return data

def process_comment(comment):
    data = {
        "id": comment.id,
        "type": "comment",
        "parent_id": comment.parent_id,
        "permalink": f"https://www.reddit.com{comment.permalink}",
        "author": str(comment.author),
        "created_utc": int(comment.created_utc),
        "score": comment.score,
        "content": clean_text(comment.body)
    }
    return data

def scrape_subreddit(subreddit_name, topic=None):
    checkpoint_file = os.path.join(BASE_DIR, f"{subreddit_name}_checkpoint.txt")
    output_file = os.path.join(BASE_DIR, f"{subreddit_name}_data.jsonl")
    processed_ids = load_checkpoints(checkpoint_file)
    subreddit = reddit.subreddit(subreddit_name)
    count = 0

    with open(output_file, 'a', encoding='utf-8') as out_f:
        if topic:
            # Search for topic in subreddit, retrieve up to 25 matching posts
            submissions = list(subreddit.search(topic, sort='relevance', limit=25))
            desc = f"Searching '{topic}' in r/{subreddit_name}"
        else:
            # Get 50 top and 50 hot posts, deduplicated
            top_posts = list(subreddit.top(limit=50))
            hot_posts = list(subreddit.hot(limit=50))
            # Use post ID to deduplicate
            seen = set()
            submissions = []
            for post in top_posts + hot_posts:
                if post.id not in seen:
                    submissions.append(post)
                    seen.add(post.id)
            desc = f"Scraping top & hot posts in r/{subreddit_name}"
        for submission in tqdm(submissions, desc=desc):
            if submission.id in processed_ids:
                continue
            data = process_submission(submission)
            out_f.write(json.dumps(data) + "\n")
            save_checkpoint(submission.id, checkpoint_file)
            count += 1
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                if comment.id in processed_ids:
                    continue
                comment_data = process_comment(comment)
                out_f.write(json.dumps(comment_data) + "\n")
                save_checkpoint(comment.id, checkpoint_file)
                count += 1
    logging.info(f"Scraped {count} items from r/{subreddit_name}")

def main():
    parser = argparse.ArgumentParser(description="Reddit Scraper")
    parser.add_argument('--topic', type=str, help='Keyword/topic to search for in subreddits')
    args = parser.parse_args()
    topic = args.topic

    with ThreadPoolExecutor(max_workers=min(8, len(SUBREDDITS))) as executor:
        futures = {executor.submit(scrape_subreddit, name, topic): name for name in SUBREDDITS if name.strip()}
        for future in as_completed(futures):
            subreddit_name = futures[future]
            try:
                future.result()
            except Exception as exc:
                logging.error(f"Subreddit {subreddit_name} generated an exception: {exc}")

if __name__ == "__main__":
    main()
