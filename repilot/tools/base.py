from abc import ABC,abstractmethod
from typing import Any

class Tool(ABC):
    name:str
    description:str
    parameters:dict[str,Any]

    def to_api_schema(self)->dict[str,Any]:
        return {
            "type":"function",
            "name":self.name,
            "description":self.description,
            "parameters":self.parameters,
        }

    @abstractmethod
    def execute(self,**kwargs:Any):
        raise NotImplementedError