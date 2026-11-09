
from pydantic import BaseModel, Field, ConfigDict


class ServiceCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10)
    category: str = Field(min_length=2, max_length=100)

    authority: str | None = None
    eligibility: str | None = None
    documents: str | None = None
    steps: str | None = None
    official_source: str | None = None


class ServiceUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = Field(default=None, min_length=10)
    category: str | None = Field(default=None, min_length=2, max_length=100)

    authority: str | None = None
    eligibility: str | None = None
    documents: str | None = None
    steps: str | None = None
    official_source: str | None = None
