from .gatherer.common import APISecrets
import os


class RedditSecrets(APISecrets):
    client_id = os.environ['REDDIT_CLIENT_ID']
    client_secret = os.environ["REDDIT_CLIENT_SECRET"]
    user_agent = os.environ["REDDIT_AGENT"]
