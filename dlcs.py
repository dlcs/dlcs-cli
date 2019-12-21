import json
import requests
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
        if not self.api.endswith("/"):
            self.api + "/"


    def ingest_image(self, image_id, image_location, **metadata):
        if not image_location.startswith("http"):
            print("Only for remote origins so far")
            raise NotImplementedError
        ops = Operations(self, metadata)
        batch = ops.ingest_from_origin(image_id, image_location)
        print(batch)
        print()
        print("done.")


    def ingest_folder(self, path_to_folder, increment_number_field="n1", **metadata):
        print("Can't yet ingest a local folder")
        raise NotImplementedError
        # ops = Operations(self, metadata)
        # ops.ingest_folder(path_to_folder, increment_number_field)


if __name__ == '__main__':
    fire.Fire(DlcsCommand)