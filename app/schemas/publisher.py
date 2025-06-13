from pydantic import BaseModel


class PublisherBase(BaseModel):
    name: str
    founding_year: int | None = None


class PublisherCreate(PublisherBase):
    pass


class PusblisherRead(PublisherBase):
    id: int


class PublisherUpdate(PublisherBase):
    pass