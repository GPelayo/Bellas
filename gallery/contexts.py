class ContextBuilder:
    reader = None
    serial_model = None

    def __init__(self):
        self._raw_data = {}

    def sync_wth_db(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError
