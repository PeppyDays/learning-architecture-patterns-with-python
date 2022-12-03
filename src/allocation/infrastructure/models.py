from __future__ import annotations

import dataclasses
import json
from datetime import date

from sqlalchemy import String, Date, Text, SmallInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass

from allocation.domain.models import Batch, OrderLine


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class BatchDataModel(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    batch_id: Mapped[str] = mapped_column(String(50), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), nullable=False)
    total_quantity: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    eta: Mapped[date | None] = mapped_column(Date)
    allocated_order_lines: Mapped[str | None] = mapped_column(Text)

    def to_domain_model(self) -> Batch:
        return Batch(
            batch_id=self.batch_id,
            sku=self.sku,
            total_quantity=self.total_quantity,
            eta=self.eta,
            allocated_order_lines=set(
                OrderLine(**line) for line in json.loads(self.allocated_order_lines)
            ),
        )

    @staticmethod
    def from_domain_model(batch: Batch) -> BatchDataModel:
        return BatchDataModel(
            batch_id=batch.batch_id,
            sku=batch.sku,
            total_quantity=batch.total_quantity,
            eta=batch.eta,
            allocated_order_lines=json.dumps(
                list(dataclasses.asdict(line) for line in batch.allocated_order_lines)
            ),
        )
