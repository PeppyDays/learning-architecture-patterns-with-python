from datetime import date

from allocation.domain.models import Batch, OrderLine
from allocation.infrastructure.repositories import BatchSqlAlchemyRepository


def test_repository_works(session):
    repository = BatchSqlAlchemyRepository(session)

    batch = Batch("batch-1", "SMALL-RED-CHAIR", 100, eta=date.today())
    order_line_1 = OrderLine("order-1", "SMALL-RED-CHAIR", 10)
    order_line_2 = OrderLine("order-2", "SMALL-RED-CHAIR", 20)

    batch.allocate(order_line_1)
    batch.allocate(order_line_2)

    repository.save(batch)


def test_repository_find_well(session):
    repository = BatchSqlAlchemyRepository(session)
    batch = repository.find_by_batch_id("batch-1")
    print(batch)


# def test_order_lines_mapper_can_load_lines(session):
#     batch_id, order_id_1, order_id_2 = [uuid.uuid4() for _ in range(3)]
#     sql = text("insert into allocation.order_lines (batch_id, order_id, sku, quantity) values (%s, %s, %s, %d)")
#     session.execute(sql, (batch_id.bytes, order_id_1.bytes, "RED-CHAIR", 12))
#     session.execute(sql, (batch_id.bytes, order_id_1.bytes, "RED-TABLE", 13))
#     session.execute(sql, (batch_id.bytes, order_id_2.bytes, "BLUE-LIPSTICK", 14))
#
#     expected = [
#         OrderLine(order_id_1.bytes, "RED-CHAIR", 12),
#         OrderLine(order_id_1.bytes, "RED-TABLE", 13),
#         OrderLine(order_id_2.bytes, "BLUE-LIPSTICK", 14),
#     ]
#
#     assert [line.to_domain_model for line in session.query(OrderLineDataModel).all()] == expected
