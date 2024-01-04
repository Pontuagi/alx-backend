#!/usr/bin/env python3

"""
A hypermedia Pagination module
"""

import csv
import math
from typing import Tuple, List, Optional, Dict


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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns the appropriate page of the dataset based on pagination
        parameters.

        Args:
        - page (int): The page number (1-indexed). Defaults to 1.
        - page_size (int): The size of each page. Defaults to 10.

        Returns:
        - List[List]: A list containing rows corresponding to requested page
        """
        assert isinstance(
            page,
            int) and page > 0, "Page number must be a positive integer."
        assert isinstance(
            page_size,
            int) and page_size > 0, "Page size must be a positive integer."

        dataset = self.dataset()
        total_rows = len(dataset)
        start_index, end_index = index_range(page, page_size)

        if start_index >= total_rows:
            return []
        return dataset[start_index:end_index + 1]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[
                str, any]:
        """Returns pagination information and the dataset page in a dictionary.

        Args:
        - page (int): The page number (1-indexed). Defaults to 1.
        - page_size (int): The size of each page. Defaults to 10.

        Returns:
        - Dict[str, any]: A dictionary containing pagination information and
        the dataset page.
        """
        dataset_page = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": len(dataset_page),
            "page": page,
            "data": dataset_page,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
