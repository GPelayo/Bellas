from bellas.celery import app
from gallery.curator import BellCurator, SubredditDoesntExistException

@app.task
def gather_pictures(subreddit, name=None, limit=10):
    try:
        gthr = BellCurator(subreddit, name)
    except SubredditDoesntExistException:
        return "Subreddit {} doesn't exist. Please check again.".format(subreddit)
    else:
        count = gthr.save_images(limit)
        return "Downloaded {} Images".format(count)
