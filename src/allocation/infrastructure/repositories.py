from sqlalchemy.orm import Session

from allocation.domain.models import Batch
from allocation.domain.repositories import BatchRepository
from allocation.infrastructure.models import BatchDataModel


class BatchSqlAlchemyRepository(BatchRepository):
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def save(self, batch: Batch) -> None:
        self._session.add(BatchDataModel.from_domain_model(batch))

    def find_by_batch_id(self, batch_id: str) -> Batch | None:
        data_model = self._session.query(BatchDataModel).filter_by(batch_id=batch_id).first()
        return data_model.to_domain_model() if data_model else None
