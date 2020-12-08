from api import DLCS

class BaseCommand(object):
    def __init__(self, dlcs: DLCS):
        self._dlcs = dlcs

