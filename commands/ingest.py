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

