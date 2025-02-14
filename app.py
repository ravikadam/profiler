import streamlit as st
# Set page config must be the first Streamlit command
st.set_page_config(page_title="Personal Prospect Profiler", layout="wide")

import os
from dotenv import load_dotenv
from utils.scraper import WebScraper
from utils.searcher import TavilySearcher
from utils.extractor import ProfileExtractor
import validators

# Load environment variables
load_dotenv()

# Initialize
@st.cache_resource
def init_clients():
    scraper = WebScraper()
    searcher = TavilySearcher(api_key=os.getenv('TAVILY_API_KEY'))
    extractor = ProfileExtractor(api_key=os.getenv('OPENAI_API_KEY'))
    return scraper, searcher, extractor

scraper, searcher, extractor = init_clients()

# Page title
st.title("Personal Prospect Profiler")

# Input
query = st.text_input("Enter person's name or profile URL:", "")

if query:
    try:
        with st.spinner("Gathering information..."):
            data_sources = []
            
            # If it's a URL, scrape it first
            if validators.url(query):
                scraped_data = scraper.scrape_website(query)
                data_sources.append({
                    'content': scraped_data['text_content'],
                    'urls': [query]
                })
            
            # Perform Tavily search
            search_data = searcher.search(query)
            if search_data['content']:
                data_sources.append(search_data)
            
            # Extract profiles from each data source
            profiles = []
            for source in data_sources:
                if source['content']:
                    profile = extractor.extract_profile(source, query)
                    profiles.append(profile)
            
            # Merge profiles
            profile = extractor.merge_profiles(profiles)
            
            # Display results in an organized layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Personal Overview")
                if profile.full_name:
                    st.subheader(profile.full_name)
                if profile.professional_headline:
                    st.write("**Professional Headline:**", profile.professional_headline)
                if profile.current_role:
                    st.write("**Current Role:**", profile.current_role)
                if profile.company:
                    st.write("**Company:**", profile.company)
                if profile.location:
                    st.write("**Location:**", profile.location)
                
                if profile.skills:
                    st.markdown("### Skills & Expertise")
                    for skill in profile.skills:
                        st.write(f"- {skill}")
                
                if profile.work_experience:
                    st.markdown("### Work Experience")
                    for exp in profile.work_experience:
                        with st.expander(f"{exp.title or 'Role'} at {exp.company or 'Company'}"):
                            if exp.duration:
                                st.write(f"**Duration:** {exp.duration}")
                            if exp.description:
                                st.write(exp.description)
                
                if profile.education:
                    st.markdown("### Education")
                    for edu in profile.education:
                        st.write(f"- **{edu.degree or 'Degree'}** from {edu.institution or 'Institution'}")
                        if edu.year:
                            st.write(f"  Year: {edu.year}")
            
            with col2:
                if profile.social_profiles:
                    st.markdown("### Online Presence")
                    for platform, link in profile.social_profiles.items():
                        st.write(f"- [{platform.title()}]({link})")
                
                if profile.websites:
                    st.markdown("### Websites")
                    for website in profile.websites:
                        st.write(f"- {website}")
                
                if profile.publications:
                    st.markdown("### Publications")
                    for pub in profile.publications:
                        with st.expander(pub.title or "Publication"):
                            if pub.year:
                                st.write(f"**Year:** {pub.year}")
                            if pub.description:
                                st.write(pub.description)
                
                if profile.speaking_engagements:
                    st.markdown("### Speaking Engagements")
                    for event in profile.speaking_engagements:
                        with st.expander(event.title or "Event"):
                            if event.date:
                                st.write(f"**Date:** {event.date}")
                            if event.description:
                                st.write(event.description)
            
            # Events Section
            st.markdown("---")
            st.header("Events & Activities")
            
            # Recent Events
            if profile.recent_events:
                st.subheader("Recent Events")
                for event in profile.recent_events:
                    with st.expander(f"{event.date or 'Recent'} - {event.title or 'Untitled Event'}"):
                        if event.description:
                            st.write(event.description)
                        if event.related_people:
                            st.write("**Related People:**", ", ".join(event.related_people))
                        if event.related_organizations:
                            st.write("**Organizations:**", ", ".join(event.related_organizations))
                        if event.url:
                            st.write(f"[More Information]({event.url})")

            # Key Events
            if profile.key_events:
                st.subheader("Key Events")
                for event in profile.key_events:
                    with st.expander(f"{event.date or 'Date Unknown'} - {event.title or 'Untitled Event'}"):
                        if event.description:
                            st.write(event.description)
                        if event.importance:
                            st.write(f"**Significance:** {event.importance}")
                        if event.related_people:
                            st.write("**Related People:**", ", ".join(event.related_people))
                        if event.related_organizations:
                            st.write("**Organizations:**", ", ".join(event.related_organizations))
                        if event.url:
                            st.write(f"[More Information]({event.url})")

            # Upcoming Events
            if profile.upcoming_events:
                st.subheader("Upcoming Events")
                for event in profile.upcoming_events:
                    with st.expander(f"{event.date or 'Upcoming'} - {event.title or 'Untitled Event'}"):
                        if event.description:
                            st.write(event.description)
                        if event.event_type:
                            st.write(f"**Type:** {event.event_type}")
                        if event.related_people:
                            st.write("**Related People:**", ", ".join(event.related_people))
                        if event.related_organizations:
                            st.write("**Organizations:**", ", ".join(event.related_organizations))
                        if event.url:
                            st.write(f"[More Information]({event.url})")
            
            # Additional Information
            if profile.key_topics:
                st.markdown("### Key Topics & Focus Areas")
                for topic in profile.key_topics:
                    st.write(f"- {topic}")
            
            if profile.achievements:
                st.markdown("### Achievements & Recognition")
                for achievement in profile.achievements:
                    st.write(f"- {achievement}")
            
            if profile.certifications:
                st.markdown("### Certifications")
                for cert in profile.certifications:
                    st.write(f"- {cert}")
            
            if profile.interesting_facts:
                st.markdown("### Interesting Facts")
                for fact in profile.interesting_facts:
                    st.write(f"- {fact}")
            
            if profile.collaborations:
                st.markdown("### Notable Collaborations")
                for collab in profile.collaborations:
                    st.write(f"- {collab}")

            # Sources and Last Update
            if profile.data_sources:
                st.markdown("---")
                st.markdown("### Data Sources")
                for source in profile.data_sources:
                    st.write(f"- {source}")

            if profile.last_updated or profile.last_known_activity_date:
                st.markdown("### Profile Information")
                if profile.last_known_activity_date:
                    st.write(f"Last Known Activity: {profile.last_known_activity_date}")
                if profile.last_updated:
                    st.write(f"Profile Last Updated: {profile.last_updated}")
                    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please make sure you have set up both OPENAI_API_KEY and TAVILY_API_KEY in your .env file")
        
st.markdown("---")
st.markdown("### How to use")
st.write("""
1. Enter a person's name, profile URL, or any identifying information
2. Wait for the analysis to complete
3. Review the extracted information about the person
""")

# Add a note about supported platforms
st.info("""
Supported inputs include:
- Names of people
- Personal websites
- Professional blogs
- LinkedIn profiles (public)
- Medium profiles
- GitHub profiles
- Academia.edu profiles
- Other public professional profiles
- News articles
- Company pages
- Conference websites
""")