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

    async def get(self):  
        if (url:=self.data.get('@id')): 
            response = await self._dlcs._get(url)
        else: 
            response = await self._dlcs.get_endpoint(self.endpoint)
        self.data = response
        return self

    async def post(self, data): 
        if (url:=self.data.get('@id')): 
            response = await self._dlcs._post(url, json=data)
        else: 
            response = await self._dlcs.post_endpoint(self.endpoint, json=data)
        self.data = response

    async def _get_stored_url(self, key:str) -> str:
        response = {}
        if (url:=self.data.get(key)): 
            response = await self._dlcs._get(url)
            response = self._dlcs.map_to_registered_model(response) 
        return response

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

