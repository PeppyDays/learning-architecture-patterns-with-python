from datetime import date, timedelta

import pytest

from allocation.domain.exceptions import OutOfStock
from allocation.domain.models import Batch, OrderLine
from allocation.domain.services import allocate


def test_allocate_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line("SMALL-TABLE", batch_quantity=20, line_quantity=2)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", batch_quantity=20, line_quantity=2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", batch_quantity=2, line_quantity=20)
    assert batch.can_allocate(line) is False


def test_can_allocate_if_available_equals_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", batch_quantity=2, line_quantity=2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-1", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    line = OrderLine("order-1", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(line) is False


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", batch_quantity=20, line_quantity=2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20


def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("ANGULAR-DESK", batch_quantity=20, line_quantity=2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("batch-1", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("batch-2", "RETRO-CLOCK", 100, eta=date.today() + timedelta(days=1))
    line = OrderLine("order-1", "RETRO-CLOCK", 10)

    allocated_batch = allocate(line, [in_stock_batch, shipment_batch])

    assert allocated_batch is in_stock_batch
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("batch-1", "MINIMALIST-SPOON", 100, eta=date.today())
    medium = Batch("batch-2", "MINIMALIST-SPOON", 100, eta=date.today() + timedelta(days=1))
    latest = Batch("batch-3", "MINIMALIST-SPOON", 100, eta=date.today() + timedelta(days=2))
    line = OrderLine("order-1", "MINIMALIST-SPOON", 10)

    allocated_batch = allocate(line, [medium, earliest, latest])

    assert allocated_batch is earliest
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch, line = make_batch_and_line("SMALL-TABLE", batch_quantity=10, line_quantity=20)

    with pytest.raises(OutOfStock, match="SMALL-TABLE"):
        allocate(line, [batch])


def make_batch_and_line(sku: str, *, batch_quantity: int, line_quantity: int) -> tuple[Batch, OrderLine]:
    return (
        Batch("batch-1", sku, batch_quantity, eta=None),
        OrderLine("order-1", sku, line_quantity),
    )
