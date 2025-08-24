import os
import json
import time
import logging
from dotenv import load_dotenv
import praw

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
SUBREDDIT = os.getenv('SUBREDDIT')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, f"{SUBREDDIT}_corpus.jsonl")
CHECKPOINT_FILE = os.path.join(BASE_DIR, f"{SUBREDDIT}_checkpoints.txt")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)

def load_checkpoints():
    if not os.path.exists(CHECKPOINT_FILE):
        return set()
    with open(CHECKPOINT_FILE, 'r') as f:
        return set(line.strip() for line in f)

def save_checkpoint(submission_id):
    with open(CHECKPOINT_FILE, 'a') as f:
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

def main():
    checkpoints = load_checkpoints()
    subreddit = reddit.subreddit(SUBREDDIT)
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as out_f:
        for submission in subreddit.top(limit=100):  # Limit to top 10 posts for speed
            if submission.id in checkpoints:
                logging.info(f"Skipping already processed submission: {submission.id}")
                continue
            try:
                out_f.write(json.dumps(process_submission(submission)) + '\n')
                submission.comments.replace_more(limit=None)
                # Get top 3 comments by score
                comments = [c for c in submission.comments.list() if hasattr(c, 'score')]
                top_comments = sorted(comments, key=lambda c: c.score, reverse=True)[:3]
                for comment in top_comments:
                    out_f.write(json.dumps(process_comment(comment)) + '\n')
                save_checkpoint(submission.id)
                logging.info(f"Processed submission: {submission.id}")
                time.sleep(2)  # Rate limit
            except Exception as e:
                logging.error(f"Error processing submission {submission.id}: {e}")
                continue

if __name__ == "__main__":
    main()
