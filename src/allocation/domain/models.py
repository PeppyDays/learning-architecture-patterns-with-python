from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class OrderLine:
    order_id: UUID
    sku: str
    quantity: int


@dataclass
class Batch:
    batch_id: UUID
    sku: str
    total_quantity: int
    eta: date | None = None
    _allocated_lines: set[OrderLine] = field(default_factory=set)

    @property
    def available_quantity(self) -> int:
        return self.total_quantity - sum(line.quantity for line in self._allocated_lines)

    def allocate(self, line: OrderLine) -> None:
        self._allocated_lines.add(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.quantity

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocated_lines:
            self._allocated_lines.remove(line)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return NotImplemented

        return self.batch_id == other.batch_id

    def __hash__(self) -> int:
        return hash(self.batch_id)
