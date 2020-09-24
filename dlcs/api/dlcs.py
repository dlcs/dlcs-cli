import requests

from .base import (
        BaseDLCS, 
        )

from ..models import (
        Batch,
        Collection, 
        Customer, 
        CustomerStorage, 
        Key, 
        Space, 
        CustomerQueue, 
        Image, 
        )

class DLCS(BaseDLCS): 
    _models = {
            Space._type: Space, 
            Collection._type: Collection, 
            Key._type: Key, 
            Customer._type: Customer, 
            CustomerQueue._type: CustomerQueue, 
            Image._type: Image
            }

    def _get_session(self): 
        session = requests.Session()
        session.auth = requests.auth.HTTPBasicAuth(
                self.key, self.secret
                )
        return session 
    
    def _close_session(self):
        if self.session is not None: 
            self.session.close()
        
    def _get(self, url, *args, **kwargs):
        response = self.session.get(url, *args, **kwargs)
        response.raise_for_status()
        return response.json()

    def _post(self, url, *args, **kwargs): 
        response = self.session.post(url, *args, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_customer(self, customer_id: int): 
        customer = Customer(dlcs=self, customer_id=customer_id)
        customer_resp = customer.get()
        customer.update_from_response(customer_resp)
        return customer
