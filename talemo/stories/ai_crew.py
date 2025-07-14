"""
CrewAI implementation for story chapter generation.
"""
import os
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from django.conf import settings

# Initialize the OpenAI model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=settings.OPENAI_API_KEY
)

def create_story_generation_crew(story_data, chapter_to_generate):
    """
    Create a CrewAI crew for generating a story chapter.
    
    Args:
        story_data (dict): Data about the story
        chapter_to_generate (dict): Data about the chapter to generate
        
    Returns:
        dict: Generated chapter with title and content
    """
    # Create the story planner agent
    story_planner = Agent(
        role="Story Planner",
        goal="Plan engaging and age-appropriate story chapters",
        backstory="""You are an expert storyteller who specializes in creating 
        engaging narratives for children. You understand story structure, character 
        development, and how to create content appropriate for different age groups.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Create the creative writer agent
    creative_writer = Agent(
        role="Creative Writer",
        goal="Write engaging, age-appropriate story content",
        backstory="""You are a talented children's book author known for your 
        vivid descriptions, engaging dialogue, and ability to create content 
        that resonates with children of different ages.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Create the title generator agent
    title_generator = Agent(
        role="Title Generator",
        goal="Create catchy, relevant chapter titles",
        backstory="""You are a specialist in creating memorable titles that 
        capture the essence of a story chapter while intriguing the reader.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Create the planning task
    planning_task = Task(
        description=f"""
        Plan a chapter for a children's story with the following details:
        - Story title: {story_data['title']}
        - Story description: {story_data['description']}
        - Age group: {story_data['age_group']}
        - Topic: {story_data['topic']}
        - Hero: {story_data['hero']}
        - Chapter location: {chapter_to_generate['place']}
        - Tool used in chapter: {chapter_to_generate['tool']}
        - Chapter order: {chapter_to_generate['order']}
        
        Create a detailed outline for this chapter that is appropriate for the age group.
        Include key plot points, character actions, and how the tool will be used.
        """,
        agent=story_planner,
        expected_output="A detailed chapter outline with plot points and character actions."
    )
    
    # Create the content writing task
    writing_task = Task(
        description=f"""
        Write a complete chapter for a children's story based on the outline provided.
        
        Story details:
        - Story title: {story_data['title']}
        - Story description: {story_data['description']}
        - Age group: {story_data['age_group']}
        - Topic: {story_data['topic']}
        - Hero: {story_data['hero']}
        - Chapter location: {chapter_to_generate['place']}
        - Tool used in chapter: {chapter_to_generate['tool']}
        - Chapter order: {chapter_to_generate['order']}
        
        Use the outline to create engaging, age-appropriate content with vivid descriptions
        and character development. The chapter should be complete with a beginning, middle, and end.
        """,
        agent=creative_writer,
        context=[planning_task],
        expected_output="A complete, engaging chapter for the children's story."
    )
    
    # Create the title generation task
    title_task = Task(
        description=f"""
        Create a catchy, relevant title for this chapter based on its content.
        
        Story details:
        - Story title: {story_data['title']}
        - Topic: {story_data['topic']}
        - Hero: {story_data['hero']}
        - Chapter location: {chapter_to_generate['place']}
        - Tool used in chapter: {chapter_to_generate['tool']}
        
        The title should be engaging, appropriate for the age group, and reflect
        the main events or theme of the chapter.
        """,
        agent=title_generator,
        context=[writing_task],
        expected_output="A catchy, relevant title for the chapter."
    )
    
    # Create the crew
    crew = Crew(
        agents=[story_planner, creative_writer, title_generator],
        tasks=[planning_task, writing_task, title_task],
        verbose=True
    )
    
    # Run the crew and get the results
    result = crew.kickoff()
    
    # Extract the title and content from the results
    # The title is the output of the title_task
    title = title_task.output
    
    # The content is the output of the writing_task
    content = writing_task.output
    
    return {
        "title": title,
        "content": content
    }