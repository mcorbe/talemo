"""
Serializers for the assets API.
"""
from rest_framework import serializers
from talemo.assets.models.asset import Asset


class AssetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Asset model.
    """
    class Meta:
        model = Asset
        fields = [
            'id', 'type', 'file_path', 'file_size', 'mime_type', 
            'source_task', 'created_at', 'metadata'
        ]
        read_only_fields = ['id', 'created_at']


class AssetCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an Asset.
    """
    class Meta:
        model = Asset
        fields = [
            'type', 'file_path', 'file_size', 'mime_type', 
            'source_task', 'metadata'
        ]


class AssetDownloadSerializer(serializers.Serializer):
    """
    Serializer for generating a download URL for an asset.
    """
    download_url = serializers.URLField()
    expires_at = serializers.DateTimeField()


class AssetUsageSerializer(serializers.Serializer):
    """
    Serializer for tenant storage usage statistics.
    """
    total_assets = serializers.IntegerField()
    total_size = serializers.IntegerField()
    by_type = serializers.DictField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )