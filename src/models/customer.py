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

    def _get_stored_url_collection_members(self, 
            url_key: str,
            dlcs_member_model):
        collection_response = self._get_stored_url(url_key)
        collection=Collection(dlcs=self._dlcs, 
                dlcs_member_model=dlcs_member_model,
                **collection_response
                )
        return collection.members()

    def portal_users(self): 
        return self._get_stored_url_collection_members(
                'portalUsers',
                PortalUser
                )

    def named_queries(self): 
        return self._get_stored_url_collection_members(
                'namedQueries',
                NamedQuery
                )

    def origin_strategies(self): 
        return self._get_stored_url_collection_members(
                'originStrategies',
                OriginStrategy
                )

    def auth_services(self): 
        return self._get_stored_url_collection_members(
                'authServices',
                AuthService
                )

    def role_providers(self): 
        return self._get_stored_url_collection_members(
                'roleProviders',
                DLCSJSONLDBase, 
                )

    def roles(self): 
        return self._get_stored_url_collection_members(
                'roles',
                Role, 
                )

    def queue(self):
        if (url:=self.data.get('queue')):
            queue = CustomerQueue(dlcs=self._dlcs, **{'@id': url})
        else: 
            queue = CustomerQueue(dlcs=self._dlcs, customer_id=self.customer_id)
        return queue

    def spaces(self):
        return self._get_stored_url_collection_members(
                'spaces',
                Space
                )

    def keys(self): 
        return self._get_stored_url_collection_members(
                'keys',
                Key
                )
    
    def storage(self): 
        storage_response = self._get_stored_url('storage')
        return CustomerStorage(dlcs=self._dlcs, **storage_response)

class Role(DLCSJSONLDBase):
    _type = 'role'

class CustomerStorage(DLCSJSONLDBase):
    _type = 'CustomerStorage'

class Key(DLCSJSONLDBase): 
    _type = 'Key'
    
    def __init__(self, dlcs=None, customer_id=None, key_id='', **kwargs):
        if key_id: 
            self.endpoint = f'/customers/{customer_id}/keys/{key_id}'
        else:
            self.endpoint = f'/customers/{customer_id}/keys'
        super().__init__(dlcs=dlcs, **kwargs)

class Space(DLCSJSONLDBase):
    _type = 'vocab:Space'

    def __init__(self, dlcs=None, customer_id=None, space_id=None, **kwargs):
        self.customer_id = customer_id
        self.space_id = space_id
        if self.customer_id: 
            self.endpoint = f'/customers/{self.customer_id}/spaces'
        if self.space_id: 
            self.endpoint = f'{self.endpoint}/{self.space_id}'
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

class PortalUser(DLCSJSONLDBase):
    _type = 'PortalUser'
    
class NamedQuery(DLCSJSONLDBase):
    _type = 'NamedQuery'

class OriginStrategy(DLCSJSONLDBase):
    _type = 'OriginStrategy'

class AuthService(DLCSJSONLDBase):
    _type = 'AuthService'
