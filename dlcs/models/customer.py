from .base import (
        DLCSJSONLDBase, 
        )

class Customer(DLCSJSONLDBase): 
    _type = 'vocab:Customer'

    def __init__(self, customer_id=None, **kwargs): 
        self.customer_id = customer_id
        if self.customer_id: 
            self.endpoint = f'/customers/{self.customer_id}'
        super().__init__(**kwargs)
    
    async def spaces(self):
        spaces = await self._get_stored_url('spaces')
        return spaces

    async def storage(self): 
        storage = await self.__get_stored_url('storage')
        return storage

    async def keys(self): 
        keys = await self._get_stored_url('keys')
        return keys

    async def roles()
        roles = await self._get_stored_url('roles')
        return roles

    async def role_providers(self): 
        role_providers = await self._get_stored_url('roleProviders')

    async def queue(self):
        if (url:=self.data.get('queue')):
            queue = CustomerQueue(dlcs=self._dlcs, **{'@id': url})
        else: 
            queue = CustomerQueue(dlcs=self._dlcs, customer_id=self.customer_id)
        return queue

class CustomerStorage(DLCSJSONLDBase):
    _type = 'CustomerStorage'

class Key(DLCSJSONLDBase): 
    _type = 'Key'

class Space(DLCSJSONLDBase):
    _type = 'vocab:Space'

    def __init__(self, customer_id=None, space_id=None, **kwargs):
        self.customer_id = customer_id
        self.space_id = space_id
        if self.customer_id and self.space_id: 
            self.endpoint = f'/customers/{self.customer_id}/spaces/{self.space_id}'
        super().__init__(**kwargs)

class CustomerQueue(DLCSJSONLDBase): 
    _type = 'vocab:CustomerQueue'

    def __init__(self, customer_id=None, **kwargs): 
        self.customer_id = customer_id
        if self.customer_id: 
            self.endpoint = f'/customers/{self.customer_id}/queue'
        super().__init__(**kwargs)

    async def post_batch(self, collection: Collection) -> Batch: 
        batch = await self._dlcs.post_endpoint(self.endpoint, json=collection.data)
        batch = Batch(dlcs=self._dlcs, **batch)
        return batch

