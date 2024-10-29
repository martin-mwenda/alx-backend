#!/usr/bin/env python3
"""
Module for pagination helper functionality.
"""
from typing import Tuple


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
