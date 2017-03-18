from urllib import request
import praw
import os
import logging
from .common import APISecrets, BaseCurator

LOG_FOLDER = "log"

if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)

bell_log = logging.getLogger("bell")
bell_log.setLevel(logging.DEBUG)

brl_log = logging.getLogger("bad-curator-urls")
brl_fl_hndlr = logging.FileHandler(os.path.join(LOG_FOLDER, "bad-urls.log"))
brl_log.addHandler(brl_fl_hndlr)
brl_log.setLevel(logging.INFO)

ALLOWED_IMAGE_EXTENTIONS = ["jpg", "png", "gif", "bmp", "jpeg"]


class RedditCurator(BaseCurator):
    def __init__(self, secrets: APISecrets, subreddit, archiver):
        super().__init__(archiver)
        self.client = praw.Reddit(client_id=secrets.client_id,
                                  client_secret=secrets.client_secret,
                                  user_agent=secrets.user_agent)
        self.subreddit = subreddit
        self.submissions = []
        self.archiver = archiver

    def gather_data(self, limit=5):
        hot_posts = self.client.subreddit(self.subreddit).hot()
        has_more_posts = True
        while len(self.submissions) < limit and has_more_posts:
            try:
                sb = next(hot_posts)
            except StopIteration:
                has_more_posts = False

            if sb.url.split(".")[-1] in ALLOWED_IMAGE_EXTENTIONS \
                    and not self.archiver.is_dupe_image(source_id=sb.id):
                self.submissions.append(sb)
            else:
                brl_log.log(logging.INFO, "Skipped {}".format(sb))

    def save_to_db(self, media_folder, subdirectory=""):
        if not os.path.exists(media_folder):
            os.mkdir(media_folder)
        for sb in self.submissions:
            filename = sb.url.split('/')[-1]
            relative_media_path = os.path.join(subdirectory, filename)
            request.urlretrieve(sb.url, os.path.join(media_folder, relative_media_path))
            self.archiver.load_image_db_data(sb, relative_media_path)
            self.archiver.save()
            bell_log.log(logging.DEBUG, relative_media_path)
