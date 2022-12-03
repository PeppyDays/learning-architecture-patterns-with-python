from typing import Iterable

from sqlalchemy.orm import Session

from allocation.domain.models import Batch
from allocation.domain.repositories import BatchRepository
from allocation.infrastructure.models import BatchDataModel


class SqlAlchemyBatchRepository(BatchRepository):
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def save(self, batch: Batch) -> None:
        data_model = BatchDataModel.from_domain_model(batch)
        self._session.add(data_model)

    def find_by_batch_id(self, batch_id: str) -> Batch | None:
        data_model = (
            self._session.query(BatchDataModel).filter_by(batch_id=batch_id).first()
        )
        return data_model.to_domain_model()

    def find_all(self) -> Iterable[Batch]:
        data_models = self._session.query(BatchDataModel).all()
        return [data_model.to_domain_model() for data_model in data_models]


class FakeBatchRepository(BatchRepository):
    _batches: list[Batch]

    def __init__(self, batches: list[Batch]):
        self._batches = batches

    def save(self, batch: Batch) -> None:
        self._batches.append(batch)

    def find_by_batch_id(self, batch_id: str) -> Batch | None:
        return next((b for b in self._batches if b.batch_id == batch_id), None)

    def find_all(self) -> Iterable[Batch]:
        return self._batches
