from bellorum.celery import app
from .gatherer.reddit import RedditGatherer, SubredditDoesntExistException
from .db.archiver import RedditImageArchiver
from bellorum.settings import MEDIA_ROOT
from .secrets import RedditSecrets
import os


REDDIT_ROOT = os.path.join("gallery", "img", "reddit")
REDDIT_FULLPATH = os.path.join(MEDIA_ROOT, REDDIT_ROOT)
if not os.path.exists(REDDIT_FULLPATH):
    os.makedirs(REDDIT_FULLPATH)


@app.task
def gather_pictures(subreddit, name=None, limit=10):
    arch = RedditImageArchiver(name or subreddit, MEDIA_ROOT)

    try:
        gthr = RedditGatherer(RedditSecrets(), subreddit, arch)
    except SubredditDoesntExistException:
        return "Subreddit {} doesn't exist. Please check again.".format(subreddit)
    else:
        gthr.gather_data(limit)
        gthr.save_to_db()
        return "Downloaded {} Images".format(len(gthr.submissions))
