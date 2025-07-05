"""
Serializers for the governance API.
"""
from rest_framework import serializers
from talemo.governance.models.parental_consent import ParentalConsent


class ParentalConsentSerializer(serializers.ModelSerializer):
    """
    Serializer for the ParentalConsent model.
    """
    class Meta:
        model = ParentalConsent
        fields = [
            'id', 'tenant', 'user', 'consenting_user', 'consent_type', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ParentalConsentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a ParentalConsent.
    """
    class Meta:
        model = ParentalConsent
        fields = ['user', 'consent_type']
    
    def create(self, validated_data):
        # Set the tenant and consenting_user fields
        validated_data['tenant'] = self.context['request'].tenant
        validated_data['consenting_user'] = self.context['request'].user
        return super().create(validated_data)


class ParentalConsentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a ParentalConsent.
    """
    class Meta:
        model = ParentalConsent
        fields = ['status']


class ParentalControlSettingsSerializer(serializers.Serializer):
    """
    Serializer for parental control settings.
    """
    max_age_range = serializers.CharField()
    content_filters = serializers.ListField(child=serializers.CharField())
    time_limits = serializers.DictField(child=serializers.IntegerField())
    

class ChildActivitySerializer(serializers.Serializer):
    """
    Serializer for child activity report.
    """
    user_id = serializers.UUIDField()
    user_name = serializers.CharField()
    stories_viewed = serializers.ListField(child=serializers.DictField())
    total_time = serializers.IntegerField()
    activity_by_day = serializers.DictField(child=serializers.IntegerField())