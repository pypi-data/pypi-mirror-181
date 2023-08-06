from pydantic import BaseModel, UUID4
from datetime import datetime, timedelta
from uuid import UUID


class Header(BaseModel):
    """
    This class serves as a model for Kafka message headers
    """

    campaign_id: UUID4
    agent: str
    start: datetime = datetime(1992, 4, 5, 2, 24)
    end: datetime = datetime(2021, 7, 14, 13, 6)

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    # @property
    # def campaign_id(self) -> UUID4:
    #     return UUID(self.raw_campaign_id.decode())
