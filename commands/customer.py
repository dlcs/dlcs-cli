import pprint
from .base import BaseCommand
from settings import DLCS_CUSTOMER_ID, DLCS_SPACE_ID
from dlcs.models import (
        Collection, 
        Customer, 
        Key, 
        CustomerQueue, 
        Space, 
        Batch
        )

class CustomerCommands(BaseCommand): 
    
    def _get_customer(self, customer_id):
        customer = Customer(dlcs=self._dlcs, customer_id=DLCS_CUSTOMER_ID)
        customer.update_from_response(customer.get())
        return customer

    def _get_customer_space(self, customer_id: int, space_id: int):
        space = Space(dlcs=self._dlcs, customer_id=customer_id, space_id=space_id)
        space.update_from_response(space.get())
        return space

    def get_default_customer(self):
        customer = self._get_customer(DLCS_CUSTOMER_ID)
        pprint.pprint(customer.data)

    def get_default_customer_space(self):
        space = self._get_customer_space(DLCS_CUSTOMER_ID, DLCS_SPACE_ID)
        pprint.pprint(space.data)

    def get_customer(self, customer_id: int):
        customer = self._get_customer(customer_id)
        return customer

    def create_customer(self, name: str, display_name: str):
        """
        POST to api to create a new customer
        :param name: path friendly name of customer
        :param display_name: display name of customer
        :return: Customer object, from json
        """
        customer_kwargs = {
                'name': name,
                'displayName': display_name, 
                }
        customer = Customer(dlcs=self._dlcs, **customer_kwargs)
        customer.update_from_response(customer.post())
        return customer

    def create_api_key(self, customer_id):
        key = Key(dlcs=self._dlcs, customer_id=customer_id)
        key.update_from_response(key.post())
        return key.data

    def create_space(self, customer_id: int, name: str):
        space_kwargs = {'name': name}
        space = Space(dlcs=self._dlcs, 
                customer_id=customer_id, 
                **space_kwargs)
        space.update_from_response(space.post())
        return space.data
