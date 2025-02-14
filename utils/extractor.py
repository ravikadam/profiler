import instructor
from openai import OpenAI
from models.profile_models import PersonProfile
from typing import Dict, Any, Union

class ProfileExtractor:
    def __init__(self, api_key: str):
        self.client = instructor.from_openai(OpenAI(api_key=api_key))

    def extract_profile(self, data: Dict[str, Any], query: str) -> PersonProfile:
        prompt = f"""
        Based on the following content about {query}, extract detailed information about the person.
        Include any available information about work experience, educational background, achievements, and interesting facts.
        If certain information is not available, skip those fields.
        
        Content: {data['content'][:6000]}  # Limiting content length for API
        
        Focus on extracting:
        1. Basic information (name, current role, location)
        2. Professional background
        3. Educational history
        4. Skills and expertise
        5. Publications or content
        6. Speaking engagements
        7. Achievements
        8. Interesting facts
        9. Key topics they focus on
        10. Professional network

        Be conservative with extractions - only include information that is clearly stated or strongly implied in the source material.
        """

        try:
            profile = self.client.chat.completions.create(
                model="gpt-4",
                response_model=PersonProfile,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Add data sources
            profile.data_sources = data.get('urls', [])
            
            return profile
            
        except Exception as e:
            raise Exception(f"Error extracting profile: {str(e)}")

    def merge_profiles(self, profiles: list[PersonProfile]) -> PersonProfile:
        """Merge multiple profiles into one, combining unique information."""
        if not profiles:
            return PersonProfile()
        
        merged = profiles[0]
        
        for profile in profiles[1:]:
            # Merge lists (with deduplication)
            merged.skills = list(set(merged.skills + profile.skills))
            merged.interests = list(set(merged.interests + profile.interests))
            merged.achievements = list(set(merged.achievements + profile.achievements))
            merged.certifications = list(set(merged.certifications + profile.certifications))
            merged.languages = list(set(merged.languages + profile.languages))
            merged.interesting_facts = list(set(merged.interesting_facts + profile.interesting_facts))
            merged.key_topics = list(set(merged.key_topics + profile.key_topics))
            merged.collaborations = list(set(merged.collaborations + profile.collaborations))
            merged.organizations = list(set(merged.organizations + profile.organizations))
            
            # Merge social profiles
            merged.social_profiles.update(profile.social_profiles)
            
            # Merge websites
            merged.websites = list(set(merged.websites + profile.websites))
            
            # Merge complex objects (work experience, education, etc.)
            merged.work_experience.extend(profile.work_experience)
            merged.education.extend(profile.education)
            merged.publications.extend(profile.publications)
            merged.speaking_engagements.extend(profile.speaking_engagements)
            
            # Update scalar fields if they're empty in merged but present in current profile
            if not merged.full_name and profile.full_name:
                merged.full_name = profile.full_name
            if not merged.professional_headline and profile.professional_headline:
                merged.professional_headline = profile.professional_headline
            if not merged.current_role and profile.current_role:
                merged.current_role = profile.current_role
            if not merged.company and profile.company:
                merged.company = profile.company
            if not merged.location and profile.location:
                merged.location = profile.location
                
            # Merge data sources
            merged.data_sources = list(set(merged.data_sources + profile.data_sources))
        
        return merged