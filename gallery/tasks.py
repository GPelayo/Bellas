from bellorum.celery import app
from gallery.curator import BellorumCurator, SubredditDoesntExistException

@app.task
def gather_pictures(subreddit, name=None, limit=10):
    try:
        gthr = BellorumCurator(subreddit, name)
    except SubredditDoesntExistException:
        return "Subreddit {} doesn't exist. Please check again.".format(subreddit)
    else:
        count = gthr.save_images(limit)
        return "Downloaded {} Images".format(count)
