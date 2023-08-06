from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class ProductControl:
    def __init__(self, block):
        self.block = block


class ProductSettingsBlock(BaseModel):
    id: str
    media: Optional[Dict[str, List[Optional[str]]]]
    price: Dict[str, Union[int, str]]
