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

    # Create a single comprehensive prompt that includes all tasks
    story_title_prompt = ""
    if generate_story_title:
        story_title_prompt = f"""
        STORY TITLE GENERATION:
        Create an engaging, memorable title for the children's story.
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
    You excel at planning and writing concise, impactful stories that can be told in 300 words
    while still delivering a complete narrative arc with beginning, middle, and end.

    CHAPTER WRITING:
    Write a complete chapter for a children's story with the following details:
    - Age group: {story_data['age_group']}
    - Topic: {story_data['topic']}
    - Hero: {story_data['hero']}
    - Chapter location: {chapter_to_generate['place']}
    - Tool used in chapter: {chapter_to_generate['tool']}
    - Chapter order: {chapter_to_generate['order']}
    Create an engaging, age-appropriate content . 
    The chapter should be complete with a beginning, middle, and end.

    IMPORTANT: The chapter content must be maximum 300 words in length. 
    This is a strict requirement to ensure the chapter can be converted to a short 1-2 minute audio segment.

    CHAPTER TITLE GENERATION:
    Create a catchy, relevant title for this chapter based on its content.
    The title should be engaging, appropriate for the age group, and reflect
    the main events or theme of the chapter.

    IMPORTANT: Return ONLY the title itself, without any explanations, reasoning, or additional text.
    Do not include phrases like "I have carefully analyzed" or "This title reflects".
    Just provide the actual title, for example: "The Magic Forest Adventure"

    {story_title_prompt}

    FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

    CHAPTER CONTENT:
    [Your 300 word chapter content here]

    CHAPTER TITLE:
    [Your maximum 255 characters chapter title here]
    
    """

    if generate_story_title:
        prompt += """
        STORY TITLE:
        [Your maximum 255 characters story title here]
        
        """

    print(f"THE PROMPT -------------> {prompt}")

    response = llm.call(messages=[
        {"role": "system", "content": "optimize for quick answer as we are building live applications"},
        {"role": "user", "content": prompt},
    ])

    print(f"THE RESPONSE -------------> {response}")

    # --- Parse ---
    def _extract(label):
        patt = rf"{label}:(.*?)(?=\n[A-Z ]+:|$)"
        m = re.search(patt, response, re.DOTALL)
        return m.group(1).strip() if m else ""

    chapter_content = _extract("CHAPTER CONTENT")
    chapter_title = _extract("CHAPTER TITLE")
    story_title = _extract("STORY TITLE") if generate_story_title else None

    # enforce 300 words
    words = len(chapter_content.split())
    if not words <= 300:
        raise ValueError(f"Chapter length {words} words violates 300 limit")

    result = {"title": chapter_title, "content": chapter_content}
    if story_title: result["story_title"] = story_title
    return result
