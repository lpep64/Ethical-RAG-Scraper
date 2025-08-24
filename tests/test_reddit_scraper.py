import os
import json
from data_acquisition.reddit_scraper import process_submission, process_comment

def test_process_submission():
    class DummySubmission:
        id = 'abc123'
        permalink = '/r/test/comments/abc123/test_post/'
        author = 'testuser'
        created_utc = 1672531200
        score = 42
        title = 'Test Title &amp; More'
        selftext = 'Test body &amp; content.'
    sub = DummySubmission()
    result = process_submission(sub)
    assert result['id'] == 'abc123'
    assert result['type'] == 'submission'
    assert result['permalink'] == 'https://www.reddit.com/r/test/comments/abc123/test_post/'
    assert result['author'] == 'testuser'
    assert result['created_utc'] == 1672531200
    assert result['score'] == 42
    assert result['title'] == 'Test Title & More'
    assert result['content'] == 'Test body & content.'

def test_process_comment():
    class DummyComment:
        id = 'def456'
        permalink = '/r/test/comments/abc123/test_post/def456/'
        author = 'commenter'
        created_utc = 1672531300
        score = 7
        body = 'Comment body &amp; here.'
    com = DummyComment()
    result = process_comment(com)
    assert result['id'] == 'def456'
    assert result['type'] == 'comment'
    assert result['permalink'] == 'https://www.reddit.com/r/test/comments/abc123/test_post/def456/'
    assert result['author'] == 'commenter'
    assert result['created_utc'] == 1672531300
    assert result['score'] == 7
    assert result['content'] == 'Comment body & here.'
