#!/usr/bin/env python3
"""
Module for pagination helper functionality.
"""
import csv
import math
from typing import Tuple, List


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for items on a specified page.

    Args:
        page (int): Page number (1-indexed).
        page_size (int): Number of items per page.

    Returns:
        Tuple[int, int]: Start and end indices for items on the page.
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
        """Loads and caches the dataset from a CSV file if not already loaded.

        Returns:
            List[List]: The cached dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header row
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieve a specific page of data.

        Args:
            page (int): Page number, default is 1.
            page_size (int): Number of items per page, default is 10.

        Returns:
            List[List]: Records on the requested page.
        """
        assert isinstance(page, int) and isinstance(page_size, int), "Argsint"
        assert page > 0 and page_size > 0, "Arguments must be positive."

        begin, stop = index_range(page, page_size)
        data = self.dataset()
        return data[begin:stop] if begin < len(data) else []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Retrieve pagination information and records for a specific page.

        Args:
            page (int): Page number, default is 1.
            page_size (int): Number of items per page, default is 10.

        Returns:
            dict: Dictionary with pagination details and records.
        """
        data = self.get_page(page, page_size)
        begin, stop = index_range(page, page_size)
        pages_count = math.ceil(len(self.__dataset) / page_size)
        info_dict = {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if stop < len(self.__dataset) else None,
            'prev_page': page - 1 if begin > 0 else None,
            'total_pages': pages_count
        }
        return info_dict
