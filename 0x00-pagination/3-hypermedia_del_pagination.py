#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination module.
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

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

    def indexed_dataset(self) -> Dict[int, List]:
        """Creates and caches an indexed version of the dataset, for
        deletion-resilient pagination.

        Returns:
            Dict[int, List]: Dataset indexed by position, up to 1000 records.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i] for i in range(
                len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Provides pagination data starting from a specific index,
        resilient to deletions.

        Args:
            index (int): Starting index for the page, default is None.
            page_size (int): Number of items per page, default is 10.

        Returns:
            Dict: Dictionary containing pagination details and data.
        """
        data = self.indexed_dataset()
        assert index >= 0 and index <= max(data.keys()), "Index out of range."

        page_index = {}
        count = index

        # Collect the items for the requested page size
        while len(page_index) < page_size and count < len(self.dataset()):
            if count in data:
                page_index[count] = data[count]
            count += 1

        page = list(page_index.values())
        page_log = page_index.keys()
        return {
            'index': index,
            'next_index': max(page_log) + 1,
            'page_size': len(page),
            'data': page
        }
