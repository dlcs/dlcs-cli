from models.base import (
        DLCSJSONLDBase, 
        )

from settings import Settings

class BaseDLCS(object):
    _models = {}

    def __init__(self, 
            settings: Settings,
            ):
        self.settings = settings
        self.session = self._get_session()

    def _get_session(self): 
        raise NotImplementedError

    def _close_session(self): 
        raise NotImplementedError

    def _get(self, url, *args, **kwargs): 
        raise NotImplementedError
        
    def _post(self, url, *args, **kwargs): 
        raise NotImplementedError
    
    def format_endpoint_url(self, endpoint): 
        return f'{self.settings.api_url}{endpoint}'
    
    def get_endpoint(self, endpoint):
        return self._get(
                self.format_endpoint_url(endpoint)
                )

    def post_endpoint(self, endpoint: str, *args, **kwargs): 
        return self._post(
                self.format_endpoint_url(endpoint), 
                *args, **kwargs
                )

    def register_model(self, model_class):
        self._models[model_class._type] = model_class

    def map_to_registered_model(self, json_data: dict): 
        registered_model = self._models.get(json_data.get('@type'), DLCSJSONLDBase)
        return registered_model(dlcs=self, **json_data)
        

