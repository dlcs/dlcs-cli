from models.base import (
        DLCSJSONLDBase, 
        )

class BaseDLCS(object): 
    api_url = ''
    key = ''
    secret = ''
    _models = {}

    def __init__(self, 
            api_url: str='', 
            key: str='', 
            secret: str='', 
            ):
        api_url = api_url.rstrip('/')
        self.api_url = api_url
        self.key = key
        self.secret = secret
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
        return f'{self.api_url}{endpoint}'
    
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
        

