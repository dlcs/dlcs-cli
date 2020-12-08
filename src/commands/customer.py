from api import DLCS

from .base import BaseCommand

from models import (
        Collection, 
        Customer, 
        Key, 
        CustomerQueue, 
        Space, 
        Batch
        )


class CustomerCommands(BaseCommand):
    def __init__(self, dlcs: DLCS, default_customer_id: int, default_space_id: int):
        BaseCommand.__init__(self, dlcs=dlcs)

        self._default_customer_id = default_customer_id
        self._default_space_id = default_space_id

    def _get_customer(self, customer_id: int):
        customer = Customer(
            dlcs=self._dlcs,
            customer_id=customer_id
        )

        customer.update_from_response(customer.get())
        return customer

    def _get_customer_space(self, customer_id: int, space_id: int):
        space = Space(
            dlcs=self._dlcs,
            customer_id=customer_id,
            space_id=space_id
        )
        space.update_from_response(space.get())
        return space

    def get_default_customer(self):
        customer = self._get_customer(
            customer_id=self._default_customer_id
        )

        return customer

    def get_default_customer_space(self):
        space = self._get_customer_space(
            customer_id=self._default_customer_id,
            space_id=self._default_space_id
        )

        return space

    def get_customer(self, customer_id: int):
        customer = self._get_customer(
            customer_id=customer_id
        )

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
        key = Key(
            dlcs=self._dlcs,
            customer_id=customer_id
        )
        key.update_from_response(key.post())
        return key.data

    def create_space(self, customer_id: int, name: str):
        space_kwargs = {'name': name}
        space = Space(dlcs=self._dlcs, 
                customer_id=customer_id, 
                **space_kwargs)
        space.update_from_response(space.post())
        return space.data
