from .base import BaseCommand

class IngestCommands(BaseCommand):

    def ingest_from_origin(self, image_id, origin, **metadata): 
        pass

    def register_collection(self, image_collection): 
        pass

    def ingest_folder(self, path_to_dir, increment_number_fields, profile, **metadata): 
        pass

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

    def _register_collection(self, image_collection):
        image_collection = Collection.from_iiif3_manifest(manifest, space=DLCS_SPACE_ID)
        queue = CustomerQueue(dlcs=self._dlcs, customer_id=DLCS_CUSTOMER_ID)
        batch = queue.post_batch(image_collection)
        return batch.data

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
        pprint.pprint(queue.to_json_dict())
        response.raise_for_status()
        batch = Batch(response.json())
        return batch

