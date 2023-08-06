from typing import Union
from time import sleep

import CoreML

from .utilities import _nsurl

class ModelConfiguration:
    def __init__(self):
        pass

class Model:
    def __init__(self, file_path: Union[str, None] = None, configuration=None):
        self.configuration = configuration
        
        if file_path is not None:
            file_url = _nsurl(file_path)

            compiled_url = None
            def compile_completion_handler(url, error):
                if error is not None:
                    raise Exception(error)
                else:
                    nonlocal compiled_url
                    compiled_url = url

            CoreML.MLModel.compileModelAtURL_completionHandler_(file_url, compile_completion_handler)
            
            while compiled_url is None:
                sleep(0.05)

            self._MLModel = CoreML.MLModel.modelWithContentsOfURL_configuration_error_(compiled_url, configuration._MLModelConfiguration if configuration is not None else None, None)[0]

    @property
    def model_description(self) -> str:
        if self._MLModel is None:
            return
        return self._MLModel.modelDescription()
    
    

    def load_from_asset(self, configuration=None):
        pass

    def load_from_file(self, file_path: str, configuration=None):
        return Model(file_path, configuration)

    def compile(self):
        pass

    def predictions_from_features(options):
        pass

    def preductions_from_batch(options):
        pass