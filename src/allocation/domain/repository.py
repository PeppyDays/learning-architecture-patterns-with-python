from typing import Protocol

from allocation.domain.models import Batch


class BatchRepository(Protocol):
    def save(self, batch: Batch):
        ...

    def find_by_identifier(self, identifier: str) -> Batch:
        ...
