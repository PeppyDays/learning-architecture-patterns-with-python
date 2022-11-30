from dataclasses import dataclass, field
from datetime import date
from typing import Any, Iterable


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

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Batch):
            return NotImplemented

        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)


def allocate(line: OrderLine, batches: Iterable[Batch]) -> Batch:
    oldest_date = date(year=1970, month=1, day=1)

    try:
        batch = next(
            b for b in sorted(batches, key=lambda b: oldest_date if b.eta is None else b.eta) if b.can_allocate(line)
        )
    except StopIteration:
        raise OutOfStock(f"Out of stock for SKU {line.sku}")

    batch.allocate(line)
    return batch


class OutOfStock(Exception):
    pass
