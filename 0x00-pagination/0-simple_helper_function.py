#!/usr/bin/env python3

"""
A simple helper function
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns the start and end index for a given page and page size.

    Args:
    - page (int): The page number (1-indexed).
    - page_size (int): The size of each page.

    Returns:
    - Tuple[int, int]: A tuple containing the start and end index.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return (start_index, end_index)
