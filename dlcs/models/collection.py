from .base import (
        DLCSJSONLDBase, 
        )

class Collection(DLCSJSONLDBase): 
    _type = 'Collection'

    def members(self):
        return [self._dlcs.map_to_registered_model(member) for member in self.data.get('member', [])] 
    
    @classmethod
    def from_iiif3_manifest(cls, iiif3_manifest: dict, **kwargs): 
        images = []
        for canvas in iiif3_manifest.get('items', []): 
            for annotation_page in canvas.get('items', []): 
                for annotation in annotation_page.get('items', []): 
                    images.append(
                            Image.from_unregistered_iiif3_image_body(
                                iiif3_image_body = annotation.get('body'), 
                                **kwargs
                            ))
        return cls(**{'member': [image.data for image in images]}) 
