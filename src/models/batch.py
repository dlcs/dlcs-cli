from .base import (
        DLCSJSONLDBase, 
        )

class Batch(DLCSJSONLDBase): 
    _type = 'Batch'

    async def images(self):
        images = await self._get_stored_url('images')
        return images

