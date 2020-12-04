from .base import (
        DLCSJSONLDBase, 
        )

class Image(DLCSJSONLDBase):
    _type = 'vocab:Image' 
    
    @classmethod
    def from_unregistered_iiif3_image_body(cls, space, iiif3_image_body):
        data = {
                'origin': iiif3_image_body.get('id'), 
                'space': space, 
                'family': 'I', 
                'mediaType' : iiif3_image_body.get('format')
                }
        return cls(**data)

    def as_registered_iiif3_image_body(self):
        """ Getting the ID here is a real hack, I'm not sure why this isn't included in the 
            DLCS Image object. 
            """
        dlcs_image_id = self.data.get('@id', '')
        dlcs_image_id_parts = dlcs_image_id.split('/')
        image_id = dlcs_image_id_parts[-1]
        space_id = dlcs_image_id_parts[-3]
        customer_id = dlcs_image_id_parts[-5]
        iiif_image_id = f'https://dlc.services/iiif-img/{customer_id}/{space_id}/{image_id}'
        return {
            "id": f'{iiif_image_id}/full/!1024,1024/0/default.jpg', 
            "type": "Image",
            "format": "image/jpg",
            "service": [{
                    "id": iiif_image_id,
                    "type": "ImageService3",
                    "profile": "level2",
                    }],
            "height": self.data.get('height'),
            "width": self.data.get('width')
            }
