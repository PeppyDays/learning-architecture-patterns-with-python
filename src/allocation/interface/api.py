from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from allocation import config
from allocation.domain.models import OrderLine
from allocation.infrastructure.repositories import SqlAlchemyBatchRepository

get_session = sessionmaker(bind=create_engine(config.get_database_url()))
app = FastAPI()


@app.post("/allocate")
def allocate_order_line(line: OrderLine):
    # line = OrderLine(request.json["orderId"], request.json["sku"], request.json["qty"])
    # session = get_session()
    # batches = SqlAlchemyBatchRepository(session).find_by_sku("sku1")
    # batch_id = allocate_order_line(line, batches, session)
    # return {"batchId": batch_id}, 201
    ...
