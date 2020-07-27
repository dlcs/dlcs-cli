from client.image import JSONLDBaseWithHydraContext, Image


class Queue(JSONLDBaseWithHydraContext):

    def __init__(self, origins: list, space, increment_number_field, family='I', **metadata):

        super(Queue, self).__init__()

        self.type = "Collection"
        self.assets = []

        for index, origin in enumerate(origins):
            # this should use Image
            asset = Image(id=origin.rsplit('/', 1)[-1],
                          space=space,
                          origin=origin,
                          tags=None,
                          string_1=metadata.get("s1", None),
                          string_2=metadata.get("s2", None),
                          string_3=metadata.get("s3", None),
                          number_1=index if increment_number_field == 'n1' else metadata.get('n1', None),
                          number_2=index if increment_number_field == 'n2' else metadata.get('n2', None),
                          number_3=index if increment_number_field == 'n3' else metadata.get('n3', None),
                          family=family)

            self.assets.append(asset)

    def to_json_dict(self):
        data = super(Queue, self).to_json_dict()
        self.add_if_not_none(data, 'member', list(map(lambda x: x.to_json_dict(), self.assets)))
        return data

# {
#     "@context": "http://www.w3.org/ns/hydra/context.jsonld",
#     "@type": "Collection",
#     "member": [
#         {
#             "id": "image-test-2",
#             "space": 1,
#             "origin": "http://tomcrane.github.io/scratch/img/IMG_4716.JPG",
#             "maxUnauthorised": -1,
#             "string1": "test 2",
#             "family": "I"
#         }
#     ]
# }
