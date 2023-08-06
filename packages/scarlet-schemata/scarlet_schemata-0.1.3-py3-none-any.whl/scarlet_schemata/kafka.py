from pydantic import BaseModel, UUID4
from datetime import datetime, timedelta
from uuid import UUID


class Header(BaseModel):
    """
    This class serves as a model for Kafka message headers
    """

    raw_campaign_id: bytes
    agent: str
    start: datetime = datetime(1992, 4, 5)
    end: datetime = datetime(2021, 7, 14)

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    @property
    def campaign_id(self) -> UUID4:
        return UUID(self.raw_campaign_id.decode())
