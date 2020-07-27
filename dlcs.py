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

    # def ingest_image(self, image_id, image_location, **metadata):
    #     if not image_location.startswith("http"):
    #         print("Only for remote origins so far")
    #         raise NotImplementedError
    #     ops = Operations(self, metadata)
    #     batch = ops.ingest_from_origin(image_id, image_location)
    #     print(batch)
    #     print()
    #     print("done.")

    # def ingest_folder(self, path_to_folder, increment_number_field="n1", **metadata):
    #     print("Can't yet ingest a local folder")
    #     raise NotImplementedError
    #     # ops = Operations(self, metadata)
    #     # ops.ingest_folder(path_to_folder, increment_number_field)


class Debug(object):

    def __init__(self, dlcscommand):
        self.dlcscommand = dlcscommand

    def settings(self):
        """
        Print current settings object being used
        :return:
        """
        print(f"api root: {self.dlcscommand.api}")
        print(f"api key: {self.dlcscommand.key}")
        print(f"api secret: {self.dlcscommand.secret[0:3]}****")
        print(f"customer: {self.dlcscommand.customer}")
        print(f"space: {self.dlcscommand.space}")


class Ingest(object):

    def __init__(self, dlcscommand):
        self.dlcscommand = dlcscommand
        self.ops = Operations(self.dlcscommand)

    def image(self, image_id, image_location, **metadata):
        if not image_location.startswith("http"):
            print("Only for remote origins so far")
            raise NotImplementedError

        batch = self.ops.ingest_from_origin(image_id, image_location, metadata)
        print(batch)
        print()
        print("done.")

    def folder(self, dir, profile='Default', increment_number_field="n1", **metadata):
        self.ops.ingest_folder(dir, increment_number_field, profile)


class Pipeline(object):

    def __init__(self):
        command = DlcsCommand()
        self.ingest = Ingest(command)
        self.customer = Customer(command)
        self.debug = Debug(command)


class Customer(object):

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
        self.ops.create_customer(name, display_name)

    def create_api_key(self):
        """
        Creates api keys for customer specified in settings
        :return:
        """
        self.ops.create_api_key()

    def create_space(self, name):
        """
        Create space for customer specified in settings
        :param name:
        :return:
        """
        self.ops.create_space(name)


if __name__ == '__main__':
    fire.Fire(Pipeline)
