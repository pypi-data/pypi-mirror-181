from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList

from typing import Union

class Sound():
    interface = RequestInterface(family="production/sound")

    # ----------------------------------------- TEMPLATE -----------------------------------------
    class Template():
        
        class Item(APIResponseItem):
            
            def __init__(self, response) -> None:
                super().__init__(response)
                self.templateName = self.data["templateName"]
                self.collections = self.data["collections"]
                self.genre = self.data["genre"]
                self.description = self.data["description"]
                self.tempo = self.data["tempo"]
                self.tags = self.data["tags"]
                

        class List(APIResponseList):
            def __init__(self, response, list_type) -> None:
                super().__init__(response, list_type)

            def resolve_item(self, list_type, item):
                if list_type == "templates":
                    return Sound.Template.Item({"data" : item})
                else:
                    raise Exception()

        @staticmethod
        def list(
            tags: Union[str, list] = "", 
            contents: Union[str, list] = "",
            collections: Union[str, list] = "",
            genre: str = "",
            tempo: str = "",
            type: str = "all"
            ) -> list:
            
            if type not in ["all", "custom", "standard"]:
                raise Exception("Invalid type supplied, should be 'all', 'custom', 'standard'")
            
            query_params = {
                "tags" : tags,
                "contents" : contents,
                "collections" : collections,
                "genre" : genre,
                "tempo" : tempo,
                "type" : type
            }
            r = Sound.interface.send_request(rtype=RequestTypes.GET, route="template", query_parameters=query_params)
            return Sound.Template.List(r, list_type="templates")
        
        def create():
            assert False, "not ready"
        def delete():
            assert False, "not ready"
        def update():
            assert False, "not ready"
    
    # ----------------------------------------- TEMPLATE SEGMENT -----------------------------------------
    class Segment():
        def create():
            route = "segment"
            assert False, "not ready"

    # ----------------------------------------- TEMPLATE PARAMETERS -----------------------------------------
    class Parameter():
        
        @staticmethod
        def get() -> dict:
            r = Sound.interface.send_request(rtype=RequestTypes.GET, route="parameter")
            return APIResponseItem(r)