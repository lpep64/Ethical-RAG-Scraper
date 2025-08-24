import os
import json
import time
import logging
from dotenv import load_dotenv
import praw
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def clean_text(text):
    return text.replace('&amp;', '&').strip()

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
        "permalink": f"https://www.reddit.com{comment.permalink}",
        "author": str(comment.author),
        "created_utc": int(comment.created_utc),
        "score": comment.score,
        "content": clean_text(comment.body)
    }
    return data


def scrape_subreddit(subreddit_name):
    subreddit_name = subreddit_name.strip()
    if not subreddit_name:
        return
    output_file = os.path.join(BASE_DIR, f"{subreddit_name}_corpus.jsonl")
    checkpoint_file = os.path.join(BASE_DIR, f"{subreddit_name}_checkpoints.txt")
    checkpoints = load_checkpoints(checkpoint_file)
    subreddit = reddit.subreddit(subreddit_name)
    count = 0
    with open(output_file, 'a', encoding='utf-8') as out_f:
        for submission in subreddit.top(limit=100):
            if submission.id in checkpoints:
                logging.info(f"Skipping already processed submission: {submission.id}")
                continue
            try:
                out_f.write(json.dumps(process_submission(submission)) + '\n')
                submission.comments.replace_more(limit=None)
                comments = [c for c in submission.comments.list() if hasattr(c, 'score')]
                top_comments = sorted(comments, key=lambda c: c.score, reverse=True)[:10]
                for comment in top_comments:
                    out_f.write(json.dumps(process_comment(comment)) + '\n')
                save_checkpoint(submission.id, checkpoint_file)
                logging.info(f"Processed submission: {submission.id} in {subreddit_name}")
                count += 1
                time.sleep(0.5)  # Reduced sleep for faster scraping
            except Exception as e:
                logging.error(f"Error processing submission {submission.id}: {e}")
                continue
    logging.info(f"Finished scraping {subreddit_name}: {count} submissions processed.")

def main():
    with ThreadPoolExecutor(max_workers=min(8, len(SUBREDDITS))) as executor:
        futures = {executor.submit(scrape_subreddit, name): name for name in SUBREDDITS if name.strip()}
        for future in as_completed(futures):
            subreddit_name = futures[future]
            try:
                future.result()
            except Exception as exc:
                logging.error(f"Subreddit {subreddit_name} generated an exception: {exc}")

if __name__ == "__main__":
    main()
