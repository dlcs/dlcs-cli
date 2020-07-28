import pprint

import fire
import settings
from operations import Operations


class DlcsCommand(object):

    def __init__(self,
                 api=settings.DLCS_ENTRY,
                 key=settings.DLCS_API_KEY,
                 secret=settings.DLCS_SECRET,
                 customer=settings.DLCS_CUSTOMER_ID,
                 space=settings.DLCS_SPACE):
        self.api = api
        self.key = key
        self.secret = secret
        self.customer = customer
        self.space = space

        self.origin = '' if not hasattr(settings, 'DLCS_ORIGIN') else settings.DLCS_ORIGIN

        if not self.api.endswith("/"):
            self.api += "/"


class Debug(object):

    def __init__(self, dlcscommand):
        self.dlcscommand = dlcscommand

    def settings(self):
        """
        Print current settings object being used
        :return:
        """
        settings_dict = {
            'api_root' : self.dlcscommand.api,
            'api_key': self.dlcscommand.key,
            'api_secret': f'{self.dlcscommand.secret[0:3]}****',
            'customer': self.dlcscommand.customer,
            'space': self.dlcscommand.space,
            'origin': self.dlcscommand.origin,
        }
        pprint.pprint(settings_dict)


class Ingest(object):
    """Operations related to ingesting assets"""

    def __init__(self, dlcscommand):
        self.dlcscommand = dlcscommand
        self.ops = Operations(self.dlcscommand)

    def image(self, image_id, location, **metadata):
        """
        Ingest a single image to DLCS, via queue
        :param image_id: Id of image to use
        :param location: Remote origin
        :param metadata: kwargs specifying metadata
        :return:
        """
        if not location.startswith("http"):
            print("Only for remote origins so far")
            raise NotImplementedError

        batch = self.ops.ingest_from_origin(image_id, location, **metadata)
        print(batch.toJSON())

    def folder(self, directory, profile='Default', increment_number_field="n1", **metadata):
        """
        Ingest entire directory of images
        :param directory:path to directory storing images
        :param profile:AWS profile to use for uploading (default 'Default')
        :param increment_number_field: metadata field to use for storing incremental number (default n1)
        :param metadata: kwargs specifying metadata, used for every image
        :return:
        """
        batch = self.ops.ingest_folder(directory, increment_number_field, profile, **metadata)
        print(batch.toJSON())


class Pipeline(object):
    """Pipeline used my Fire to group all request"""

    def __init__(self):
        command = DlcsCommand()
        self.ingest = Ingest(command)
        self.customer = Customer(command)
        self.debug = Debug(command)


class Customer(object):
    """Operations related to customer"""

    def __init__(self, dlcscommand):
        self.dlcscommand = dlcscommand
        self.ops = Operations(self.dlcscommand)

    def create(self, name, display_name):
        """
        Create a new customer with specified name.
        NOTE: Requires admin credentials
        :param name: url-param name of customer
        :param display_name: 'friendly' name of customer
        :return:
        """
        customer = self.ops.create_customer(name, display_name)
        pprint.pprint(customer)

    def create_api_key(self):
        """
        Creates api keys for customer specified in settings
        :return:
        """
        key = self.ops.create_api_key()
        pprint.pprint(key)

    def create_space(self, name):
        """
        Create space for customer specified in settings
        :param name: name to use for space
        :return:
        """
        space = self.ops.create_space(name)
        pprint.pprint(space)


if __name__ == '__main__':
    fire.Fire(Pipeline)
