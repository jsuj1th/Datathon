"""
Job data model using Pydantic for validation and serialization
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, field_validator
from enum import Enum


class JobType(str, Enum):
    """Job type enumeration"""
    NEW_GRAD = "new_grad"
    INTERNSHIP = "internship"
    ENTRY_LEVEL = "entry_level"
    EXPERIENCED = "experienced"


class RemoteOption(str, Enum):
    """Remote work options"""
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"


class CollectionMethod(str, Enum):
    """Method used to collect the job"""
    MCP_GITHUB = "mcp_github"
    WEB_SCRAPING = "web_scraping"
    API = "api"


class Job(BaseModel):
    """
    Unified job posting schema
    """
    # Required fields
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job title/position")
    apply_link: str = Field(..., description="Application URL")

    # Optional core fields
    location: Optional[str] = Field(None, description="Job location (city, state, country)")
    salary: Optional[str] = Field(None, description="Salary range or compensation")
    description: Optional[str] = Field(None, description="Full job description")

    # Additional details
    requirements: Optional[List[str]] = Field(None, description="Required skills/qualifications")
    benefits: Optional[List[str]] = Field(None, description="Benefits offered")
    job_type: Optional[JobType] = Field(JobType.NEW_GRAD, description="Type of position")
    experience_level: Optional[str] = Field(None, description="Required experience level")

    # Dates
    posted_date: Optional[str] = Field(None, description="When the job was posted")
    deadline: Optional[str] = Field(None, description="Application deadline")
    days_since_posted: Optional[int] = Field(None, description="Days since posting")

    # Work arrangement
    remote_option: Optional[RemoteOption] = Field(RemoteOption.UNKNOWN, description="Remote work availability")
    visa_sponsorship: Optional[bool] = Field(None, description="Whether visa sponsorship is offered")

    # Metadata (collection information)
    source: str = Field(..., description="Source of the job posting")
    collection_method: CollectionMethod = Field(..., description="How the job was collected")
    collected_at: datetime = Field(default_factory=datetime.now, description="When this job was collected")

    # Additional tags
    field: Optional[str] = Field(None, description="Field/domain (e.g., AI/ML, Backend, Frontend)")
    company_type: Optional[str] = Field(None, description="Company type (e.g., startup, FAANG, enterprise)")

    @field_validator('company', 'position')
    @classmethod
    def clean_text(cls, v: str) -> str:
        """Clean and normalize text fields"""
        if v:
            return v.strip()
        return v

    @field_validator('apply_link')
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Ensure URL is valid"""
        if not v.startswith('http'):
            raise ValueError('apply_link must be a valid URL starting with http')
        return v

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "company": "Google",
                "position": "Machine Learning Engineer - New Grad",
                "apply_link": "https://careers.google.com/jobs/12345",
                "location": "Mountain View, CA",
                "salary": "$150k - $200k",
                "description": "Build ML models at scale...",
                "requirements": ["Python", "TensorFlow", "BS in CS"],
                "job_type": "new_grad",
                "remote_option": "hybrid",
                "visa_sponsorship": True,
                "source": "speedyapply/2026-AI-College-Jobs",
                "collection_method": "mcp_github",
                "field": "AI/ML"
            }
        }


class JobCollection(BaseModel):
    """
    Collection of jobs with metadata
    """
    jobs: List[Job]
    total_count: int
    collection_timestamp: datetime = Field(default_factory=datetime.now)
    sources: List[str]

    def to_json_file(self, filepath: str, pretty: bool = True):
        """Save collection to JSON file"""
        import json

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(
                self.model_dump(mode='json'),
                f,
                indent=2 if pretty else None,
                ensure_ascii=False,
                default=str
            )

    @classmethod
    def from_job_list(cls, jobs: List[Job]):
        """Create collection from list of jobs"""
        sources = list(set(job.source for job in jobs))
        return cls(
            jobs=jobs,
            total_count=len(jobs),
            sources=sources
        )
