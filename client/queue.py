from client.image import JSONLDBaseWithHydraContext, Image


class Queue(JSONLDBaseWithHydraContext):

    def __init__(self, origins: list, space: int, increment_number_field: str, family='I', **metadata):

        super(Queue, self).__init__()

        self.type = "Collection"
        self.assets = []

        for index, origin in enumerate(origins):
            asset = Image(id=Image.get_image_id(origin),
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
