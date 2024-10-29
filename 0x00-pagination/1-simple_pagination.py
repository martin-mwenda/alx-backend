#!/usr/bin/env python3
"""
Module for pagination helper functionality.
"""
import csv
import math
from typing import Tuple, List


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate start and end index for items on a given page.

    Args:
        page (int): Page number (1-indexed).
        page_size (int): Number of items per page.

    Returns:
        Tuple[int, int]: Start and end index for items on the page.
    """
    begin = (page - 1) * page_size
    stop = begin + page_size
    return (begin, stop)


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Returns a cached dataset, loading it from a CSV file if needed."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header row
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a specific page of data.

        Args:
            page (int): Page number, default is 1.
            page_size (int): Number of items per page, default is 10.

        Returns:
            List[List]: The list of records on the requested page.
        """
        assert isinstance(page, int) and isinstance(page_size, int), "Arg int"
        assert page > 0 and page_size > 0, "Arguments must be positive."

        begin, stop = index_range(page, page_size)
        data = self.dataset()
        return data[begin:stop] if begin < len(data) else []
