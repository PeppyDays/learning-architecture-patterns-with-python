from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


@dataclass
class Batch:
    batch_id: str
    sku: str
    total_quantity: int
    eta: date | None = None
    allocated_order_lines: set[OrderLine] = field(default_factory=set)

    @property
    def available_quantity(self) -> int:
        return self.total_quantity - sum(line.quantity for line in self.allocated_order_lines)

    def allocate(self, line: OrderLine) -> None:
        self.allocated_order_lines.add(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.quantity

    def deallocate(self, line: OrderLine) -> None:
        if line in self.allocated_order_lines:
            self.allocated_order_lines.remove(line)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return NotImplemented

        return self.batch_id == other.batch_id

    def __hash__(self) -> int:
        return hash(self.batch_id)
