"""
Implementation of various agents for CrewAI integration.
"""
from .base import BaseAgent
from crewai import Task
import logging

logger = logging.getLogger(__name__)

class ModerationAgent(BaseAgent):
    """
    Agent responsible for ensuring content safety and appropriateness.
    """
    def __init__(self, verbose=True):
        super().__init__(
            name="Moderator",
            role="Content Moderator and Safety Expert",
            goal="Ensure all content is safe, appropriate, and follows guidelines",
            backstory=(
                "You are an expert content moderator with years of experience in "
                "reviewing children's content. You have a keen eye for identifying "
                "inappropriate material, sensitive topics, and potential issues that "
                "might not be suitable for young audiences. You understand the importance "
                "of maintaining a safe environment while still allowing for creativity "
                "and educational value."
            ),
            verbose=verbose
        )
    
    def create_moderation_task(self, content, age_range="4-8"):
        """
        Create a task for moderating content.
        
        Args:
            content (str): The content to moderate
            age_range (str, optional): The target age range for the content
            
        Returns:
            Task: A CrewAI task for content moderation
        """
        return Task(
            description=(
                f"Review the following content for appropriateness for children aged {age_range}: "
                f"'{content}'. Check for inappropriate language, themes, violence, scary content, "
                "or any other material that might not be suitable for the specified age range. "
                "Provide a detailed assessment and recommendation."
            ),
            expected_output=(
                "A moderation report with: 1) Approval status (approved/rejected), "
                "2) Detailed reasoning, 3) Specific issues identified (if any), "
                "4) Suggested modifications to make the content appropriate (if applicable)."
            ),
            agent=self.agent
        )


class TTSAgent(BaseAgent):
    """
    Agent responsible for converting text to speech.
    """
    def __init__(self, verbose=True):
        super().__init__(
            name="Voice Synthesizer",
            role="Text-to-Speech Specialist",
            goal="Convert text to natural-sounding speech with appropriate expression",
            backstory=(
                "You are a specialist in text-to-speech technology with expertise in "
                "creating natural-sounding narrations. You understand how to process "
                "text to add appropriate pauses, emphasis, and emotional tone. You "
                "specialize in French voice synthesis and can select the most appropriate "
                "voice for different types of content and age groups."
            ),
            verbose=verbose
        )
    
    def create_tts_task(self, text, voice_params=None):
        """
        Create a task for text-to-speech conversion.
        
        Args:
            text (str): The text to convert to speech
            voice_params (dict, optional): Parameters for voice selection and configuration
            
        Returns:
            Task: A CrewAI task for TTS conversion
        """
        voice_params = voice_params or {}
        voice_type = voice_params.get('voice_type', 'neutral')
        language = voice_params.get('language', 'fr-FR')
        
        return Task(
            description=(
                f"Convert the following text to speech using a {voice_type} voice in {language}: "
                f"'{text}'. Process the text to identify appropriate pauses, emphasis, and "
                "emotional tone. Prepare the text for optimal TTS processing by adding "
                "SSML markers where needed."
            ),
            expected_output=(
                "Processed text with SSML markup for optimal TTS conversion, including: "
                "1) Appropriate pauses, 2) Emphasis markers, 3) Emotional tone indicators, "
                "4) Pronunciation guidance for difficult words."
            ),
            agent=self.agent
        )


class QuotaAgent(BaseAgent):
    """
    Agent responsible for enforcing tenant quotas.
    """
    def __init__(self, verbose=True):
        super().__init__(
            name="Quota Manager",
            role="Resource Allocation Specialist",
            goal="Enforce tenant quotas and optimize resource usage",
            backstory=(
                "You are a meticulous resource manager responsible for ensuring fair "
                "allocation of system resources. You track usage patterns, enforce "
                "quota limits, and help optimize resource consumption. Your expertise "
                "helps maintain system stability while providing the best possible "
                "experience for all users within their plan limitations."
            ),
            verbose=verbose
        )
    
    def create_quota_check_task(self, tenant_id, resource_type, requested_amount):
        """
        Create a task for checking quota compliance.
        
        Args:
            tenant_id (str): The ID of the tenant
            resource_type (str): The type of resource being requested
            requested_amount (int): The amount of the resource being requested
            
        Returns:
            Task: A CrewAI task for quota checking
        """
        return Task(
            description=(
                f"Check if tenant {tenant_id} has sufficient quota for {requested_amount} "
                f"units of {resource_type}. Analyze current usage patterns, subscription "
                "level, and available quota. Provide a decision on whether to allow the "
                "request and include relevant usage statistics."
            ),
            expected_output=(
                "A quota assessment with: 1) Approval status (approved/rejected), "
                "2) Current usage statistics, 3) Remaining quota after this request, "
                "4) Recommendations for optimizing usage if quota is running low."
            ),
            agent=self.agent
        )


class EmbeddingAgent(BaseAgent):
    """
    Agent responsible for generating vector embeddings for semantic search and duplication detection.
    """
    def __init__(self, verbose=True):
        super().__init__(
            name="Embedding Specialist",
            role="Vector Embedding and Semantic Analysis Expert",
            goal="Create high-quality vector embeddings for content search and similarity detection",
            backstory=(
                "You are an expert in natural language processing and vector embeddings. "
                "Your specialty is converting text into meaningful vector representations "
                "that capture semantic meaning. Your work enables powerful semantic search, "
                "content recommendation, and duplicate detection capabilities. You understand "
                "the nuances of different embedding models and how to optimize them for "
                "specific use cases."
            ),
            verbose=verbose
        )
    
    def create_embedding_task(self, content, embedding_type="story"):
        """
        Create a task for generating vector embeddings.
        
        Args:
            content (str): The content to embed
            embedding_type (str, optional): The type of content being embedded
            
        Returns:
            Task: A CrewAI task for embedding generation
        """
        return Task(
            description=(
                f"Generate vector embeddings for the following {embedding_type} content: "
                f"'{content}'. Process the content to extract key semantic features and "
                "create a high-quality vector representation. Also check for potential "
                "duplicates or highly similar content in the existing database."
            ),
            expected_output=(
                "An embedding analysis with: 1) Processed content ready for embedding, "
                "2) Key semantic features identified, 3) Similarity assessment with existing content, "
                "4) Recommendations for metadata tagging based on content analysis."
            ),
            agent=self.agent
        )


class StoryCompanion(BaseAgent):
    """
    Agent responsible for assisting users in creating and developing stories.
    """
    def __init__(self, verbose=True):
        super().__init__(
            name="Story Companion",
            role="Creative Writing Assistant and Story Development Guide",
            goal="Help users create engaging and age-appropriate stories",
            backstory=(
                "You are a friendly and creative writing assistant specialized in helping "
                "families create wonderful stories together. You have extensive knowledge "
                "of storytelling techniques, character development, and narrative structures "
                "appropriate for children. You excel at guiding users through the creative "
                "process, offering suggestions, and helping refine ideas into compelling stories."
            ),
            verbose=verbose
        )
    
    def create_story_assistance_task(self, prompt=None, partial_story=None, assistance_type="ideation"):
        """
        Create a task for providing story creation assistance.
        
        Args:
            prompt (str, optional): The initial story prompt or idea
            partial_story (str, optional): Partially completed story that needs assistance
            assistance_type (str, optional): Type of assistance needed (ideation, development, refinement)
            
        Returns:
            Task: A CrewAI task for story assistance
        """
        if assistance_type == "ideation":
            description = (
                "Help the user develop a story idea based on the following prompt: "
                f"'{prompt or 'No specific prompt provided'}'. Suggest potential characters, "
                "settings, themes, and plot elements that would make an engaging children's story. "
                "Provide multiple options to inspire creativity."
            )
            expected_output = (
                "Story ideation suggestions including: 1) 2-3 potential story directions, "
                "2) Character ideas with brief descriptions, 3) Setting possibilities, "
                "4) Themes appropriate for children, 5) Questions to help the user develop their idea further."
            )
        elif assistance_type == "development":
            description = (
                "Help the user develop their partial story further: "
                f"'{partial_story}'. Suggest ways to expand the narrative, develop characters, "
                "enhance the setting, and create an engaging plot arc. Provide specific "
                "suggestions that maintain the user's creative direction."
            )
            expected_output = (
                "Story development suggestions including: 1) Plot continuation ideas, "
                "2) Character development opportunities, 3) Setting enrichment, "
                "4) Potential story complications and resolutions, 5) Dialogue suggestions."
            )
        elif assistance_type == "refinement":
            description = (
                "Help the user refine and improve their story: "
                f"'{partial_story}'. Provide feedback on narrative flow, character consistency, "
                "age-appropriateness, engagement, and overall quality. Suggest specific "
                "improvements while preserving the user's creative voice."
            )
            expected_output = (
                "Story refinement feedback including: 1) Strengths of the current story, "
                "2) Areas for improvement, 3) Specific editing suggestions, "
                "4) Age-appropriateness assessment, 5) Overall enhancement recommendations."
            )
        else:
            description = (
                "Provide general story creation assistance based on the user's needs. "
                f"Consider the following context: Prompt: '{prompt or 'None'}', "
                f"Partial story: '{partial_story or 'None'}'. Offer helpful guidance, "
                "suggestions, and feedback to support the user's creative process."
            )
            expected_output = (
                "Helpful story assistance including: 1) Relevant suggestions based on user context, "
                "2) Creative ideas to inspire the user, 3) Constructive feedback if applicable, "
                "4) Questions to guide further development, 5) Encouragement and support."
            )
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=self.agent
        )