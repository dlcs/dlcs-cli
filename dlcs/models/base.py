import json

class DLCSJSONLDBase(object): 
    context = "http://www.w3.org/ns/hydra/context.jsonld"
    _id = None
    _type = None
    endpoint = None

    def __init__(self, dlcs=None, **kwargs):
        self._dlcs = dlcs
        self._initial_data = {
                '@context': self.context,  
                '@type': self._type
                }

        self.data = {**self._initial_data, **kwargs}

    def update_from_response(self, response): 
        self.data = response
        return self

    def get(self):  
        if (url:=self.data.get('@id')): 
            return self._dlcs._get(url)
        else: 
            return self._dlcs.get_endpoint(self.endpoint)

    def post(self, data=None): 
        if not data:
            data = self.data
        if (url:=self.data.get('@id')): 
            return self._dlcs._post(url, json=data)
        else: 
            return self._dlcs.post_endpoint(self.endpoint, json=data)

    def _get_stored_url(self, key:str) -> str:
        if (url:=self.data.get(key)): 
            return self._dlcs._get(url)
        else: 
            print(f'{key} not present in {self}')

    def to_json_dict(self):
        data = {}
        self.add_if_not_none(data, '@context', self.context)
        self.add_if_not_none(data, '@id', self.at_id)
        self.add_if_not_none(data, 'id', self.id)
        self.add_if_not_none(data, '@type', self.type)
        return data

    def as_json(self, **kwargs):
        return json.dumps(self.to_json_dict(), **kwargs)

    @staticmethod
    def add_if_not_none(dictionary, key, value, wrap=lambda x: x):
        if value is not None:
            dictionary[key] = wrap(value)

