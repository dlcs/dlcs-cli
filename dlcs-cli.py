import pprint
import fire
import settings

from dlcs.api import DLCS
from commands import (
        IngestCommands, 
        CustomerCommands
        )

class Debug(object):

    def __init__(self, dlcs):
        self._dlcs = dlcs

    def settings(self):
        """
        Print current settings object being used
        :return:
        """
        settings_dict = {
            'dlcs.api_url' : self._dlcs.api_url,
            'dlcs.key': self._dlcs.key,
            'dlcs.secret': f'{self._dlcs.secret[0:3]}****',
            #'customer': self.dlcscommand.customer,
            #'space': self.dlcscommand.space,
            #'origin': self.dlcscommand.origin,
        }
        pprint.pprint(settings_dict)

class Pipeline(object):
    """Pipeline used by Python Fire to group all request"""

    def __init__(self):
        dlcs = DLCS(
                api_url=settings.DLCS_API_URL, 
                key=settings.DLCS_KEY, 
                secret=settings.DLCS_SECRET, 
                )
        self.customer = CustomerCommands(dlcs)
        self.ingest = IngestCommands(dlcs)
        self.debug = Debug(dlcs)

if __name__ == '__main__':
    fire.Fire(Pipeline)
