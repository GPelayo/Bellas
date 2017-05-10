from urllib import request
import praw
from prawcore import exceptions
from gallery.media_storage.s3 import S3Apdater
from .common import APISecrets, BaseGatherer
from gallery.logger import BellLogger

ALLOWED_IMAGE_EXTENTIONS = ["jpg", "png", "gif", "bmp", "jpeg"]

logger = BellLogger("bad-urls", default_level="INFO")


class SubredditDoesntExistException(Exception):
    def __init__(self, subreddit_name):
        self.message = "Subreddit '{}' doesn't exist.".format(subreddit_name)

    def __str__(self):
        return self.message


class RedditGatherer(BaseGatherer):
    def __init__(self, secrets: APISecrets, subreddit, archiver):
        super().__init__(archiver)
        self.client = praw.Reddit(client_id=secrets.client_id,
                                  client_secret=secrets.client_secret,
                                  user_agent=secrets.user_agent)
        self.subreddit = subreddit
        self.submissions = []
        self.archiver = archiver

        try:
            self.archiver.description = self.client.subreddit(self.subreddit).public_description
        except exceptions.Redirect:
            raise SubredditDoesntExistException(subreddit)

    def gather_data(self, limit=5):
        top_posts = self.client.subreddit(self.subreddit).top()
        has_more_posts = True
        while len(self.submissions) < limit and has_more_posts:
            try:
                sb = next(top_posts)
            except StopIteration:
                has_more_posts = False

            if sb.url.split(".")[-1] in ALLOWED_IMAGE_EXTENTIONS \
                    and not self.archiver.is_dupe_image(source_id=sb.id):
                self.submissions.append(sb)
            else:
                logger.log("Skipped {}".format(sb))

    #TODO split to "save to media" and "save to_db"
    def save_to_db(self):
        for sb in self.submissions:
            filename = sb.url.split('/')[-1]
            response = request.urlopen(sb.url)
            adpt = S3Apdater()
            adpt.stream_to_storage(response, filename)
            self.archiver.load_image_db_data(sb, adpt.get_url(filename))
            self.archiver.save()
            logger.log(adpt.get_url(filename))
