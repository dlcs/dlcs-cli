import pprint
from .base import BaseCommand
from settings import DLCS_CUSTOMER_ID, DLCS_SPACE_ID
from dlcs.models import (
        Collection, 
        Customer, 
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
        pprint.pprint(customer.data)

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
        return customer.data

    def create_api_key(self):
        url = f'{self.dlcscommand.api}customers/{self.dlcscommand.customer}/keys'
        response = post(url, json={}, auth=self._get_auth())
        response.raise_for_status()
        return response.json()

    def create_space(self, name: str):
        body = {"@type": "Space", "name": name}
        url = f'{self.dlcscommand.api}customers/{self.dlcscommand.customer}/spaces'
        response = post(url, json=body, auth=self._get_auth())
        response.raise_for_status()
        return response.json()


class Customefadsr(object):
    """Operations related to customer"""

    def __init__(self, dlcscommand):
        self.dlcscommand = dlcscommand
        self.ops = Operations(self.dlcscommand)

    def create(self, name, display_name):
        """
        Create a new customer with specified name.
        NOTE: Requires admin credentials
        :param name: url-param name of customer
        :param display_name: 'friendly' name of customer
        :return:
        """
        customer = self.ops.create_customer(name, display_name)
        pprint.pprint(customer)

    def create_api_key(self):
        """
        Creates api keys for customer specified in settings
        :return:
        """
        key = self.ops.create_api_key()
        pprint.pprint(key)

    def create_space(self, name):
        """
        Create space for customer specified in settings
        :param name: name to use for space
        :return:
        """
        space = self.ops.create_space(name)
        pprint.pprint(space)


