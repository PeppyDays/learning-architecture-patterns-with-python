from sqlalchemy.orm import Session

from allocation.domain.models import OrderLine
from allocation.domain.services import allocate
from allocation.domain.repositories import BatchRepository


def allocate_order_line(
    line: OrderLine, repository: BatchRepository, session: Session
) -> str:
    batches = list(repository.find_by_sku(line.sku))
    batch = allocate(line, batches)
    session.commit()
    return batch.batch_id
