from py_metarium import (
    Being
)


class Decoder:

    def __init__(self, url=None) -> None:
        url = url or None
        assert url is not None
        being_initialization_parameters = {
            "timeline": {
                "type": "substrate",
                "parameters": {
                    "url" : url
                }
            }
        }

        b = Being(**being_initialization_parameters)

        self.metarium_node = b.timeline_portal
    
    def info(self):
        return self.metarium_node.info()

    def decode(self, direction, block_hash=None, block_count=None):
        return self.metarium_node.get_points(direction=direction, block_hash=block_hash, block_count=block_count)
