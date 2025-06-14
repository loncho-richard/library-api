from pydantic import BaseModel


class PublisherBase(BaseModel):
    name: str
    founding_year: int | None = None


class PublisherCreate(PublisherBase):
    pass


class PublisherRead(PublisherBase):
    id: int


class PublisherUpdate(BaseModel):
    name: str | None = None
    founding_year: int | None = None