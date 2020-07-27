from client.batch import Batch
from client.image import Image, ImageCollection
from requests import post, auth


class Operations(object):

    def __init__(self, dlcscommand):
        self.dlcscommand = dlcscommand

    def make_image(self, image_id, origin, metadata):
        image = Image(id=image_id,
                      space=self.dlcscommand.space,
                      origin=origin,
                      tags=None,
                      string_1=metadata.get("s1", None),
                      string_2=metadata.get("s2", None),
                      string_3=metadata.get("s3", None),
                      number_1=metadata.get("n1", None),
                      number_2=metadata.get("n2", None),
                      number_3=metadata.get("n3", None))
        return image

    def ingest_from_origin(self, image_id, origin):
        image = self.make_image(image_id, origin)
        coll = ImageCollection(images=[image])
        batch = self.register_collection(coll)
        return batch

    # def ingest_folder(path_to_folder, increment_number_field):
    #    pass

    def register_collection(self, image_collection):
        authorisation = auth.HTTPBasicAuth(self.dlcscommand.key, self.dlcscommand.secret)
        url = self.dlcscommand.api + 'customers/' + str(self.dlcscommand.customer) + '/queue'
        body = image_collection.to_json_dict()
        response = post(url, json=body, auth=authorisation)
        batch = Batch(response.json())

        return batch

    def create_customer(self, name: str, display_name: str):
        """
        POST to api to create a new customer
        :param name: path friendly name of customer
        :param display_name: display name of customer
        :return: Customer object, from json
        """
        body = {"name": name, "displayName": display_name}
        url = f'{self.dlcscommand.api}customers'
        response = post(url, json=body, auth=self._get_auth())
        response.raise_for_status()
        print(f"Created customer '{name}':")
        print(response.status_code)
        print(response.json())

    def create_api_key(self):
        url = f'{self.dlcscommand.api}customers/{self.dlcscommand.customer}/keys'
        response = post(url, json={}, auth=self._get_auth())
        response.raise_for_status()
        print(f"Created api_keys for customer '{self.dlcscommand.customer}':")
        print(response.status_code)
        print(response.json())

    def create_space(self, name: str):
        body = {"@type": "Space", "name": name}
        url = f'{self.dlcscommand.api}customers/{self.dlcscommand.customer}/spaces'
        response = post(url, json=body, auth=self._get_auth())
        response.raise_for_status()
        print(f"Created space for customer '{self.dlcscommand.customer}':")
        print(response.status_code)
        print(response.json())

    def _get_auth(self):
        return auth.HTTPBasicAuth(self.dlcscommand.key, self.dlcscommand.secret)