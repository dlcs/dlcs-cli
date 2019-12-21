
from client.batch import Batch
from client.image import Image, ImageCollection
from requests import post, auth

class Operations(object):

    def __init__(self, dlcscommand, metadata):
        self.dlcscommand = dlcscommand
        self.metadata = metadata

    def make_image(self, image_id, origin):
        md = self.metadata
        image = Image(id=image_id, 
                      space=self.dlcscommand.space,
                      origin=origin,
                      tags=None,
                      string_1=md.get("s1", None),
                      string_2=md.get("s2", None),
                      string_3=md.get("s3", None),
                      number_1=md.get("n1", None),
                      number_2=md.get("n2", None),
                      number_3=md.get("n3", None))
        return image


    def ingest_from_origin(self, image_id, origin):
        image = self.make_image(image_id, origin)
        coll = ImageCollection(images = [image])
        batch = self.register_collection(coll)
        return batch


    # def ingest_folder(path_to_folder, increment_number_field):
    #    pass


    def register_collection(self, image_collection):
        authorisation = auth.HTTPBasicAuth(self.dlcscommand.key, self.dlcscommand.secret)
        url = self.dlcscommand.api + 'customers/' + str(self.dlcscommand.customer) + '/queue'
        json = image_collection.to_json_dict()
        response = post(url, json=json, auth=authorisation)
        batch = Batch(response.json())

        return batch