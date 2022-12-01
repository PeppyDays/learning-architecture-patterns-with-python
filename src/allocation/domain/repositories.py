import abc

from allocation.domain.models import Batch


class BatchRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, batch: Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_batch_id(self, batch_id: str) -> Batch:
        raise NotImplementedError
