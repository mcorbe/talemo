"""
Tests for the stories app.
"""
import json
from unittest.mock import patch
from django.test import TestCase
from .models.story import Story
from .models.chapter import Chapter
from .services import generate_story_chapter

class StoryChapterGenerationTest(TestCase):
    @patch('talemo.stories.ai_crew.create_story_generation_crew')
    def test_generate_story_chapter(self, mock_create_crew):
        # Mock the create_story_generation_crew function
        mock_create_crew.return_value = {
            "title": "The First Painting",
            "content": "Lucy took the paintbrush to her room and started to paint..."
        }

        # Test data
        test_data = {
            "story": {
                "title": "The Magic Paintbrush",
                "description": "A tale about creativity and believing in oneself",
                "age_group": "6-8 years",
                "topic": "Art and Imagination",
                "hero": "Lucy",
                "chapters": [
                    {
                        "title": "The Discovery",
                        "place": "Grandmother's Attic",
                        "tool": "Paintbrush",
                        "order": 1,
                        "content": "Lucy was exploring her grandmother's attic when she found an old wooden chest..."
                    },
                    {
                        "title": "The First Painting",
                        "place": "Lucy's Room",
                        "tool": "Magic Paintbrush",
                        "order": 2
                    }
                ]
            }
        }

        # Call the function in synchronous mode
        result = generate_story_chapter(test_data, async_mode=False)

        # Verify the result
        self.assertEqual(result['title'], "The First Painting")
        self.assertEqual(result['place'], "Lucy's Room")
        self.assertEqual(result['tool'], "Magic Paintbrush")
        self.assertEqual(result['order'], 2)
        self.assertTrue(result['content'])  # Content should not be empty

        # Verify that the story and chapters were created in the database
        story = Story.objects.get(title="The Magic Paintbrush")
        self.assertEqual(story.description, "A tale about creativity and believing in oneself")
        self.assertEqual(story.age_group, "6-8 years")
        self.assertEqual(story.topic, "Art and Imagination")
        self.assertEqual(story.hero, "Lucy")

        chapters = Chapter.objects.filter(story=story).order_by('order')
        self.assertEqual(chapters.count(), 2)

        first_chapter = chapters[0]
        self.assertEqual(first_chapter.title, "The Discovery")
        self.assertEqual(first_chapter.place, "Grandmother's Attic")
        self.assertEqual(first_chapter.tool, "Paintbrush")
        self.assertEqual(first_chapter.order, 1)
        self.assertEqual(first_chapter.content, "Lucy was exploring her grandmother's attic when she found an old wooden chest...")

        second_chapter = chapters[1]
        self.assertEqual(second_chapter.title, "The First Painting")
        self.assertEqual(second_chapter.place, "Lucy's Room")
        self.assertEqual(second_chapter.tool, "Magic Paintbrush")
        self.assertEqual(second_chapter.order, 2)
        self.assertTrue(second_chapter.content)  # Content should not be empty

    def test_generate_story_chapter_missing_fields(self):
        # Test data with missing required fields
        test_data = {
            "story": {
                "title": "The Magic Paintbrush",
                "description": "A tale about creativity and believing in oneself",
                # Missing age_group
                "topic": "Art and Imagination",
                "hero": "Lucy",
                "chapters": [
                    {
                        "title": "The Discovery",
                        "place": "Grandmother's Attic",
                        "tool": "Paintbrush",
                        "order": 1,
                        "content": "Lucy was exploring her grandmother's attic when she found an old wooden chest..."
                    }
                ]
            }
        }

        # Call the function in synchronous mode and expect a ValueError
        with self.assertRaises(ValueError):
            generate_story_chapter(test_data, async_mode=False)

    def test_generate_story_chapter_all_chapters_have_content(self):
        # Test data where all chapters already have content
        test_data = {
            "story": {
                "title": "The Magic Paintbrush",
                "description": "A tale about creativity and believing in oneself",
                "age_group": "6-8 years",
                "topic": "Art and Imagination",
                "hero": "Lucy",
                "chapters": [
                    {
                        "title": "The Discovery",
                        "place": "Grandmother's Attic",
                        "tool": "Paintbrush",
                        "order": 1,
                        "content": "Lucy was exploring her grandmother's attic when she found an old wooden chest..."
                    },
                    {
                        "title": "The First Painting",
                        "place": "Lucy's Room",
                        "tool": "Magic Paintbrush",
                        "order": 2,
                        "content": "Lucy took the paintbrush to her room and started to paint..."
                    }
                ]
            }
        }

        # Call the function in synchronous mode and expect a ValueError
        with self.assertRaises(ValueError):
            generate_story_chapter(test_data, async_mode=False)

    @patch('talemo.stories.ai_crew.create_story_generation_crew')
    def test_generate_story_title_for_first_chapter(self, mock_create_crew):
        # Mock the create_story_generation_crew function to return a story title
        mock_create_crew.return_value = {
            "title": "The First Adventure",
            "content": "Once upon a time, in a small village, there lived a brave child named Max...",
            "story_title": "The Magical Journey of Max"
        }

        # Test data with a placeholder story title and first chapter
        test_data = {
            "story": {
                "title": "Untitled Story",
                "description": "A tale of adventure and discovery",
                "age_group": "8-10 years",
                "topic": "Adventure",
                "hero": "Max",
                "chapters": [
                    {
                        "place": "Small Village",
                        "tool": "Magic Map",
                        "order": 1
                    }
                ]
            }
        }

        # Call the function in synchronous mode
        result = generate_story_chapter(test_data, async_mode=False)

        # Verify that the story title was updated
        story = Story.objects.get(hero="Max")
        self.assertEqual(story.title, "The Magical Journey of Max")

        # Verify that the chapter was created correctly
        chapter = Chapter.objects.get(story=story)
        self.assertEqual(chapter.title, "The First Adventure")
        self.assertEqual(chapter.place, "Small Village")
        self.assertEqual(chapter.tool, "Magic Map")
        self.assertEqual(chapter.order, 1)
        self.assertTrue(chapter.content)  # Content should not be empty
