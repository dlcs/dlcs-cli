from .base import (
        DLCSJSONLDBase, 
        )
from .collection import (
        Collection, 
        )
from .batch import (
        Batch, 
        )

class Customer(DLCSJSONLDBase): 
    _type = 'vocab:Customer'

    def __init__(self, dlcs=None, customer_id=None, **kwargs): 
        self.customer_id = customer_id
        if self.customer_id: 
            self.endpoint = f'/customers/{self.customer_id}'
        super().__init__(dlcs=dlcs, **kwargs)
    
    def spaces(self):
        return self._get_stored_url('spaces')
    
    def storage(self): 
        return self.__get_stored_url('storage')

    def keys(self): 
        return self._get_stored_url('keys')

    def roles(self):
        return self._get_stored_url('roles')

    def queue(self):
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

    def __init__(self, dlcs=None, customer_id=None, space_id=None, **kwargs):
        self.customer_id = customer_id
        self.space_id = space_id
        if self.customer_id and self.space_id: 
            self.endpoint = f'/customers/{self.customer_id}/spaces/{self.space_id}'
        super().__init__(dlcs=dlcs, **kwargs)

class CustomerQueue(DLCSJSONLDBase): 
    _type = 'vocab:CustomerQueue'

    def __init__(self, dlcs=None, customer_id=None, **kwargs): 
        self.customer_id = customer_id
        if self.customer_id: 
            self.endpoint = f'/customers/{self.customer_id}/queue'
        super().__init__(dlcs=dlcs, **kwargs)

    def post_batch(self, collection: Collection) -> Batch: 
        batch = self._dlcs.post_endpoint(self.endpoint, json=collection.data)
        batch = Batch(dlcs=self._dlcs, **batch)
        return batch

