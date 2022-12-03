from datetime import date
from typing import Iterable

from allocation.domain.exceptions import OutOfStock
from allocation.domain.models import Batch, OrderLine


def allocate(line: OrderLine, batches: Iterable[Batch]) -> Batch:
    try:
        batch = next(
            b
            for b in sorted(batches, key=lambda b: date.min if b.eta is None else b.eta)
            if b.can_allocate(line)
        )
    except StopIteration:
        raise OutOfStock(f"Out of stock for SKU {line.sku}")

    batch.allocate(line)
    return batch
