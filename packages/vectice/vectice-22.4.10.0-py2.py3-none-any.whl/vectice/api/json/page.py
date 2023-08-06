from dataclasses import dataclass
from typing import Optional


@dataclass
class Page:
    """
    simple structure to allow paging when requesting list of elements
    """

    index: Optional[int] = 1
    """
    the index of the page
    """
    size: Optional[int] = 100
    """
    the size of the page.
    """
    afterCursor: Optional[bool] = False

    hasNextPage: Optional[bool] = False
