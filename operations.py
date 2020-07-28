import pprint

from botocore.exceptions import ClientError

from client.batch import Batch
from client.image import Image, ImageCollection
from client.queue import Queue

from requests import post, auth
import boto3
import os


class Operations(object):

    def __init__(self, dlcscommand):
        self.dlcscommand = dlcscommand

    def make_image(self, image_id, origin, **metadata):
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

    def ingest_from_origin(self, image_id, origin, **metadata):
        image = self.make_image(image_id, origin, **metadata)
        coll = ImageCollection(images=[image])
        batch = self.register_collection(coll)
        return batch

    def register_collection(self, image_collection):
        url = self.dlcscommand.api + 'customers/' + str(self.dlcscommand.customer) + '/queue'
        body = image_collection.to_json_dict()
        response = post(url, json=body, auth=self._get_auth())
        batch = Batch(response.json())
        return batch

    def ingest_folder(self, dir, increment_number_field, profile, **metadata):
        if self.dlcscommand.origin == '':
            raise Exception('No origin set')

        session = boto3.Session(profile_name=profile)
        s3 = session.client('s3')
        key_prefix = f'{self.dlcscommand.customer}/{self.dlcscommand.space}/'
        bucket = self.dlcscommand.origin

        uploaded = [];

        for filename in os.listdir(dir):
            full_path = os.path.join(dir, filename)
            key = f'{key_prefix}{filename}'
            try:
                response = s3.upload_file(full_path, bucket, key)
                # TODO - assumes eu-west-1
                public_url = f'https://{bucket}.s3-eu-west-1.amazonaws.com/{key}'
                uploaded.append(public_url)
                print(f'uploaded: {public_url}..')
            except ClientError as e:
                print(f'failed to upload {filename}..')

        if not uploaded:
            print("Nothing uploaded. Nothing to do.")
            return

        queue = Queue(uploaded, self.dlcscommand.space, increment_number_field, "I", **metadata)
        url = f'{self.dlcscommand.api}customers/{self.dlcscommand.customer}/queue'
        response = post(url, json=queue.to_json_dict(), auth=self._get_auth())
        response.raise_for_status()
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
        return response.json()

    def create_api_key(self):
        url = f'{self.dlcscommand.api}customers/{self.dlcscommand.customer}/keys'
        response = post(url, json={}, auth=self._get_auth())
        response.raise_for_status()
        return response.json()

    def create_space(self, name: str):
        body = {"@type": "Space", "name": name}
        url = f'{self.dlcscommand.api}customers/{self.dlcscommand.customer}/spaces'
        response = post(url, json=body, auth=self._get_auth())
        response.raise_for_status()
        return response.json()

    def _get_auth(self):
        return auth.HTTPBasicAuth(self.dlcscommand.key, self.dlcscommand.secret)