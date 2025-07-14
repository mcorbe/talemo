"""
Single LLM call implementation for story chapter generation.
"""
import os
import re
from crewai import LLM
from django.conf import settings

def create_story_generation_crew(story_data, chapter_to_generate, generate_story_title=False):
    """
    Generate a story chapter using a single LLM call.

    Args:
        story_data (dict): Data about the story
        chapter_to_generate (dict): Data about the chapter to generate
        generate_story_title (bool): Whether to generate a story title

    Returns:
        dict: Generated chapter with title and content, and optionally a story title
    """

    # Initialize the LLM
    llm = LLM(
        model=settings.OPENAI_MODEL_NAME,
        base_url=settings.OPENAI_API_BASE
    )

    print(settings.OPENAI_API_KEY)

    # Create a single comprehensive prompt that includes all tasks
    story_title_prompt = ""
    if generate_story_title:
        story_title_prompt = f"""
        4. STORY TITLE GENERATION:
        Create an engaging, memorable title for the children's story based on the following details:
        - Description: {story_data['description']}
        - Age group: {story_data['age_group']}
        - Topic: {story_data['topic']}
        - Hero: {story_data['hero']}
        - First chapter location: {chapter_to_generate['place']}
        - Tool used in first chapter: {chapter_to_generate['tool']}

        The title should be captivating, appropriate for the age group, and reflect
        the overall theme and essence of the story. It should appeal to children
        and make them want to read the story.

        IMPORTANT: Return ONLY the title itself, without any explanations, reasoning, or additional text.
        Do not include phrases like "I have carefully analyzed" or "This title reflects".
        Just provide the actual title, for example: "The Magical Adventures of {story_data['hero']}"
        """

    prompt = f"""
    You are an expert children's storyteller who specializes in creating engaging narratives for children.
    You understand story structure, character development, and how to create content appropriate for different age groups.
    You excel at planning and writing concise, impactful stories that can be told in 150-300 words
    while still delivering a complete narrative arc with beginning, middle, and end.

    Please complete the following tasks in order:

    1. CHAPTER PLANNING:
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

    IMPORTANT: Plan for a concise chapter that will be 150-300 words in length, as the final
    chapter will be limited to this word count to create a short 1-2 minute audio segment.

    2. CHAPTER WRITING:
    Based on your outline, write a complete chapter for the children's story.
    Use the outline to create engaging, age-appropriate content with vivid descriptions
    and character development. The chapter should be complete with a beginning, middle, and end.

    IMPORTANT: The chapter content must be between 150-300 words in length. This is a strict requirement
    to ensure the chapter can be converted to a short 1-2 minute audio segment.

    3. CHAPTER TITLE GENERATION:
    Create a catchy, relevant title for this chapter based on its content.
    The title should be engaging, appropriate for the age group, and reflect
    the main events or theme of the chapter.

    IMPORTANT: Return ONLY the title itself, without any explanations, reasoning, or additional text.
    Do not include phrases like "I have carefully analyzed" or "This title reflects".
    Just provide the actual title, for example: "Chapter {chapter_to_generate['order']} - The Magic Forest Adventure"

    {story_title_prompt}

    FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

    CHAPTER CONTENT:
    [Your 150-300 word chapter content here]

    CHAPTER TITLE:
    [Your chapter title here, format: "Chapter {chapter_to_generate['order']} - Title"]

    {f"STORY TITLE:\n[Your story title here]" if generate_story_title else ""}
    """

    # Make a single call to the LLM
    response = llm.chat_completion([{"role": "user", "content": prompt}])
    response_text = response.choices[0].message.content

    # Parse the response to extract the different parts
    chapter_content = ""
    chapter_title = ""
    story_title = ""

    # Extract chapter content
    content_match = re.search(r'CHAPTER CONTENT:(.*?)(?=CHAPTER TITLE:|$)', response_text, re.DOTALL)
    if content_match:
        chapter_content = content_match.group(1).strip()

    # Extract chapter title
    title_match = re.search(r'CHAPTER TITLE:(.*?)(?=STORY TITLE:|$)', response_text, re.DOTALL)
    if title_match:
        raw_title = title_match.group(1).strip()
        # Extract the actual title from the verbose response
        chapter_title_match = re.search(r'Chapter \d+ - (.+?)(?:\n|$)', raw_title)
        if chapter_title_match:
            chapter_title = chapter_title_match.group(1).strip()
        else:
            # If no "Chapter X - " pattern is found, use the raw title
            chapter_title = raw_title

    # Extract the story title if needed
    if generate_story_title:
        story_title_match = re.search(r'STORY TITLE:(.*?)(?=$)', response_text, re.DOTALL)
        if story_title_match:
            story_title = story_title_match.group(1).strip()

    # Prepare the result
    result = {
        "title": chapter_title,
        "content": chapter_content
    }

    # Add the story title if it was generated
    if generate_story_title and story_title:
        result["story_title"] = story_title

    print(result)

    return result
