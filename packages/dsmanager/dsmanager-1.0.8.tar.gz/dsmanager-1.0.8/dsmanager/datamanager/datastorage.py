"""@Author: Rayane AMROUCHE

Datastorage Class
"""

import json
from typing import Any


class DataStorage(dict):
    """A dictionary that can be accessed through attributes"""

    def __dir__(self):
        return sorted(set(dir(super()) + list(self.keys())))

    def __getattr__(self, __name: str) -> Any:
        return self[__name]

    def __repr__(self) -> str:
        return json.dumps(self, indent=4)
