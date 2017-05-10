from .gatherer.common import APISecrets
from bellorum import settings
import os


class RedditSecrets(APISecrets):
    if settings.USING_LOCAL_SETTINGS:
        client_id = settings.REDDIT_CLIENT_ID
        client_secret = settings.REDDIT_CLIENT_SECRET
        user_agent = settings.REDDIT_USER_AGENT
    else:
        client_id = os.environ['REDDIT_CLIENT_ID']
        client_secret = os.environ["REDDIT_CLIENT_SECRET"]
        user_agent = os.environ["REDDIT_AGENT"]
