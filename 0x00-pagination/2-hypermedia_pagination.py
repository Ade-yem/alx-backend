#!/usr/bin/env python3
"""Hypermedia pagination"""

import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """return a tuple of size two containing a start index and
    an end index corresponding to the range
    of indexes to return in a list for those particular pagination params"""
    start_index = (page - 1) * page_size
    end_index = page * page_size
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
        """Get the contents of a page"""
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        try:
            dataset = self.dataset()
            rng = index_range(page, page_size)
            return dataset[rng[0]:rng[1]]
        except IndexError:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """returns a dictionary containing key-value pairs"""
        total = len(self.dataset())
        total_pages = (total + page_size - 1) // page_size
        prev_page = page - 1 if page > 1 else None
        next_page = page + 1 if self.get_page(page, page_size) != [] else None
        size = page_size if self.get_page(page, page_size) != [] else 0
        return {
            "page_size": size,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": int(total_pages)
        }
