from .base import (
        DLCSJSONLDBase, 
        )
from .image import Image

class Collection(DLCSJSONLDBase): 
    _type = 'Collection'

    def __init__(self, dlcs=None, dlcs_member_model=None, **kwargs): 
        self.dlcs_member_model = dlcs_member_model
        super().__init__(dlcs=dlcs, **kwargs)
        
    def members(self):
        return [self.dlcs_member_model(member) for member in self.data.get('member', [])] 
    
    @classmethod
    def from_iiif3_manifest(cls, iiif3_manifest: dict, dlcs=None, **kwargs): 
        images = []
        for canvas in iiif3_manifest.get('items', []): 
            for annotation_page in canvas.get('items', []): 
                for annotation in annotation_page.get('items', []): 
                    images.append(
                            Image.from_unregistered_iiif3_image_body(
                                iiif3_image_body = annotation.get('body'), 
                                **kwargs
                            ))
        return cls(dlcs=dlcs, dlcs_member_model=Image, **{'member': [image.data for image in images]}) 
