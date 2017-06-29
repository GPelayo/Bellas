import praw
from urllib.request import urlopen
from urllib.error import URLError
from prawcore import exceptions
from .common import BaseGalleryController
from gallery.logger import BellLogger
from gallery.secrets import RedditSecrets
from gallery.db.parcel.models import GalleryParcel, WebImageParcel

logger = BellLogger("bad-urls", file_name="bad-urls.log", default_level="INFO")


class SubredditDoesntExistException(Exception):
    def __init__(self, subreddit_name):
        self.message = "Subreddit '{}' doesn't exist.".format(subreddit_name)

    def __str__(self):
        return self.message


class RedditOrderType:
    TOP = 1


class RedditGatherer(BaseGalleryController):
    DEFAULT_GATHER_LIMIT = 10

    def __init__(self, subreddit_name, gallery_name=None, sort_order=RedditOrderType.TOP, image_filter=lambda x: True):
        secrets = RedditSecrets()
        self.client = praw.Reddit(client_id=secrets.client_id,
                                  client_secret=secrets.client_secret,
                                  user_agent=secrets.user_agent)
        self.subreddit_name = subreddit_name
        self.sort_order = sort_order
        self.gallery_name = gallery_name or subreddit_name
        self.image_filter = image_filter
        try:
            self.client.subreddit(self.subreddit_name)
        except exceptions.Redirect:
            raise SubredditDoesntExistException(subreddit_name)

    def build_gallery(self, limit=DEFAULT_GATHER_LIMIT):
        subreddit = self.client.subreddit(self.subreddit_name)

        glry = GalleryParcel()
        glry.name = self.gallery_name or self.subreddit_name
        glry.description = subreddit.public_description

        # if self.sort_order == RedditOrderType.TOP:
        submission_stream = self.client.subreddit(self.subreddit_name).top()
        has_more_posts = True

        while glry.image_count < limit and has_more_posts:
            try:
                sb = next(submission_stream)
            except StopIteration:
                has_more_posts = False

            img = WebImageParcel()

            img.name = sb.title
            img.source_id = sb.id
            img.source_url = sb.url

            if not self.image_filter(img):
                logger.log("{} skipped by image_filter ".format(sb.title))
            elif self.validate_url(img.source_url):
                glry.add_image(img)

        return glry

    def validate_url(self, url):
        try:
            urlopen(url)
        except URLError as m:
            logger.log("[{}] {}: {}".format(self.subreddit_name, url, str(m)))
        else:
            return True
