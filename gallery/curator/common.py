class BaseCurator:
    def __init__(self, archiver):
        self.archiver = archiver


class APISecrets:
    client_id = None
    client_secret = None
    user_agent = None
