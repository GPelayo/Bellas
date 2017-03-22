from bellorum.celery import app
from .curator.reddit import RedditCurator
from .db.archiver import RedditImageArchiver
from .secrets import RedditSecrets
from bellorum.settings import MEDIA_ROOT
import os
import praw


REDDIT_ROOT = os.path.join("gallery", "img", "reddit")
REDDIT_FULLPATH = os.path.join(MEDIA_ROOT, REDDIT_ROOT)
if not os.path.exists(REDDIT_FULLPATH):
    os.mkdir(REDDIT_FULLPATH)


@app.task
def gather_pictures(subreddit, name=None):
    arch = RedditImageArchiver(name or subreddit, MEDIA_ROOT)
    crtr = RedditCurator(RedditSecrets(), subreddit, arch)
    crtr.gather_data(10)

    sbr_folder = os.path.join(REDDIT_ROOT, subreddit)

    crtr.save_to_db(MEDIA_ROOT, sbr_folder)

    return "Downloaded {} Images".format(len(crtr.submissions))
