import aiohttp

from .base import (
        BaseDLCS, 
        )

import ..models as dlcs_models

from ..models import (
        Customer, 
        Space, 
        Collection, 
        Key, 
        CustomerQueue, 
        Batch, 
        Image
        )

class AIODLCS(BaseDLCS): 
    _models = {
            Space._type: Space, 
            Collection._type: Collection, 
            Key._type: Key, 
            Customer._type: Customer, 
            CustomerQueue._type: CustomerQueue, 
            Image._type: Image
            }

    def _get_session(self): 
        return aiohttp.ClientSession(
                raise_for_status=True, 
                auth=aiohttp.BasicAuth(
                    login=self.key, 
                    password=self.secret, 
                    )
                )
    
    async def _close_session(self):
        if self.session is not None: 
            _ = await self.session.close()
            return _
        
    async def _get(self, url, *args, **kwargs):
        response = await self.session.get(url, *args, **kwargs)
        response.raise_for_status()
        response_json = await response.json()
        return response_json

    async def _post(self, url, *args, **kwargs): 
        response = await self.session.post(url, *args, **kwargs)
        response.raise_for_status()
        response_json = await response.json()
        return response_json

    async def get_customer(self, customer_id: int): 
        customer = Customer(dlcs=self, customer_id=customer_id)
        customer = await customer.get()
        return customer
