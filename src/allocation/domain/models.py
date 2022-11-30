from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    identifier: str
    sku: str
    quantity: int


@dataclass
class Batch:
    identifier: str
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

        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)
