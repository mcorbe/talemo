"""
Serializers for the stories API.
"""
from rest_framework import serializers
from talemo.stories.models.story import Story
from talemo.stories.models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'category']
        read_only_fields = ['id']


class StorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Story model.
    """
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Story
        fields = [
            'id', 'title', 'description', 'content', 'image', 'audio', 
            'user_audio', 'language', 'age_range', 'duration', 'tags', 
            'created_by', 'visibility', 'is_published', 'is_ai_generated', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class StoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Story.
    """
    class Meta:
        model = Story
        fields = [
            'title', 'description', 'content', 'image', 'audio', 
            'language', 'age_range', 'visibility', 'is_published', 
            'is_ai_generated'
        ]
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class StoryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a Story.
    """
    class Meta:
        model = Story
        fields = [
            'title', 'description', 'content', 'image', 'audio', 
            'language', 'age_range', 'visibility', 'is_published', 
            'is_ai_generated'
        ]


class StoryVisibilitySerializer(serializers.ModelSerializer):
    """
    Serializer for updating a Story's visibility.
    """
    class Meta:
        model = Story
        fields = ['visibility']