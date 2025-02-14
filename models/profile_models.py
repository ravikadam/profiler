from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class WorkExperience(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None

class Publication(BaseModel):
    title: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None

class Event(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    event_type: Optional[str] = None  # e.g., "professional", "personal", "achievement"
    importance: Optional[str] = None  # e.g., "high", "medium", "low"
    url: Optional[str] = None
    related_people: List[str] = Field(default_factory=list)
    related_organizations: List[str] = Field(default_factory=list)

class PersonProfile(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name of the person")
    professional_headline: Optional[str] = Field(None, description="Professional title or headline")
    current_role: Optional[str] = Field(None, description="Current job role")
    company: Optional[str] = Field(None, description="Current company")
    location: Optional[str] = Field(None, description="Geographic location")
    
    # Professional Background
    work_experience: List[WorkExperience] = Field(default_factory=list, description="List of work experiences")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    skills: List[str] = Field(default_factory=list, description="Professional skills and expertise")
    
    # Online Presence
    social_profiles: Dict[str, str] = Field(default_factory=dict, description="Social media profiles")
    websites: List[str] = Field(default_factory=list, description="Personal or professional websites")
    
    # Content and Interests
    publications: List[Publication] = Field(default_factory=list, description="Articles, papers, or other publications")
    speaking_engagements: List[Event] = Field(default_factory=list, description="Speaking events or presentations")
    interests: List[str] = Field(default_factory=list, description="Professional and personal interests")
    
    # Achievements and Recognition
    achievements: List[str] = Field(default_factory=list, description="Notable achievements and awards")
    certifications: List[str] = Field(default_factory=list, description="Professional certifications")
    
    # Additional Insights
    languages: List[str] = Field(default_factory=list, description="Languages spoken")
    interesting_facts: List[str] = Field(default_factory=list, description="Interesting or unique facts about the person")
    key_topics: List[str] = Field(default_factory=list, description="Key topics or themes the person focuses on")
    
    # Network
    collaborations: List[str] = Field(default_factory=list, description="Notable collaborations or partnerships")
    organizations: List[str] = Field(default_factory=list, description="Professional organizations or memberships")
    
    # Events
    key_events: List[Event] = Field(
        default_factory=list, 
        description="Significant events in the person's career or life"
    )
    recent_events: List[Event] = Field(
        default_factory=list, 
        description="Recent events or activities (within last 6 months)"
    )
    upcoming_events: List[Event] = Field(
        default_factory=list,
        description="Scheduled future events or announced plans"
    )
    
    # Timeline context
    last_known_activity_date: Optional[str] = Field(
        None,
        description="Date of most recent known activity or update"
    )
    
    # Sources
    data_sources: List[str] = Field(default_factory=list, description="Sources of the information")
    last_updated: Optional[str] = Field(
        None,
        description="When this profile was last updated"
    )

    def add_event(self, event: Event, event_type: str = "recent"):
        """Add an event to the appropriate category based on its type and date"""
        if event_type == "key":
            self.key_events.append(event)
        elif event_type == "recent":
            self.recent_events.append(event)
        elif event_type == "upcoming":
            self.upcoming_events.append(event)

    def sort_events(self):
        """Sort all event lists by date"""
        for event_list in [self.key_events, self.recent_events, self.upcoming_events]:
            event_list.sort(
                key=lambda x: datetime.strptime(x.date, "%Y-%m-%d") if x.date else datetime.max,
                reverse=True
            )

    class Config:
        arbitrary_types_allowed = True