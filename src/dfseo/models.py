"""Pydantic models for DataForSEO API responses."""

from typing import Any

from pydantic import BaseModel, Field, field_validator


class OrganicResult(BaseModel):
    """Organic SERP result."""

    rank: int
    rank_group: int = Field(alias="rank_group")
    domain: str
    url: str
    title: str
    description: str | None = None
    breadcrumb: str | None = None


class FeaturedSnippet(BaseModel):
    """Featured snippet result."""

    text: str
    source_url: str = Field(alias="source_url")
    source_domain: str = Field(alias="source_domain")


class PeopleAlsoAskItem(BaseModel):
    """People Also Ask item."""

    question: str
    expanded_text: str = Field(alias="expanded_text")


class SerpFeatures(BaseModel):
    """Collection of SERP features."""

    featured_snippet: FeaturedSnippet | None = None
    people_also_ask: list[PeopleAlsoAskItem] = Field(default_factory=list)
    local_pack: bool = False
    knowledge_graph: bool = False
    top_stories: bool = False
    images: bool = False
    videos: bool = False
    shopping: bool = False


class SerpResult(BaseModel):
    """Parsed SERP result."""

    keyword: str
    location: str
    language: str
    device: str
    results_count: int = Field(alias="results_count")
    serp_features: list[str] = Field(default_factory=list)
    organic_results: list[OrganicResult] = Field(default_factory=list)
    featured_snippet: FeaturedSnippet | None = None
    people_also_ask: list[PeopleAlsoAskItem] = Field(default_factory=list)
    cost: float = 0.0
    timestamp: str


class Location(BaseModel):
    """Location item."""

    location_code: int = Field(alias="location_code")
    location_name: str = Field(alias="location_name")
    location_code_parent: int | None = Field(alias="location_code_parent", default=None)
    country_iso_code: str | None = Field(alias="country_iso_code", default=None)
    location_type: str | None = Field(alias="location_type", default=None)


class Language(BaseModel):
    """Language item."""

    language_name: str = Field(alias="language_name")
    language_code: str = Field(alias="language_code")


class UserData(BaseModel):
    """User data from API."""

    login: str
    balance: float
    rate_limit: int = Field(alias="rate_limit")


class ApiTask(BaseModel):
    """API task structure."""

    id: str | None = None
    status_code: int = Field(alias="status_code")
    status_message: str | None = Field(alias="status_message", default=None)
    result: list[dict[str, Any]] = Field(default_factory=list)

    @field_validator("result", mode="before")
    @classmethod
    def coerce_null_result(cls, v: Any) -> list:
        """Convert null API result to empty list."""
        return v if v is not None else []


class ApiResponse(BaseModel):
    """Base API response."""

    status_code: int = Field(alias="status_code")
    status_message: str | None = Field(alias="status_message", default=None)
    tasks: list[ApiTask] = Field(default_factory=list)
    cost: float | None = None
    time: str | None = None
