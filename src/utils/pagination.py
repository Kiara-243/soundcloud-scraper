from dataclasses import dataclass
from typing import Optional

@dataclass
class Paginator:
    """
    Simple paginator to control page-based requests and global max_items.

    - end_page <= 0 means unlimited pages.
    - max_items is the global cap for total items; None means unlimited.
    """

    end_page: int = 0
    max_items: Optional[int] = None
    current_page: int = 0
    items_yielded: int = 0

    def can_fetch_next_page(self) -> bool:
        if self.end_page > 0 and self.current_page >= self.end_page:
            return False
        if self.max_items is not None and self.items_yielded >= self.max_items:
            return False
        return True

    def start_new_page(self) -> None:
        self.current_page += 1

    def register_items(self, count: int) -> None:
        if count < 0:
            count = 0
        self.items_yielded += count

    def reached_max_items(self) -> bool:
        return self.max_items is not None and self.items_yielded >= self.max_items