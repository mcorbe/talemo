"""
Views for the assets API.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from talemo.assets.models.asset import Asset
from .serializers import (
    AssetSerializer, 
    AssetCreateSerializer, 
    AssetDownloadSerializer,
    AssetUsageSerializer
)


class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint for assets.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all assets for the currently authenticated user's tenant.
        """
        return Asset.objects.filter(tenant=self.request.tenant)

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return AssetCreateSerializer
        elif self.action == 'download':
            return AssetDownloadSerializer
        return AssetSerializer

    def perform_create(self, serializer):
        """
        Set the tenant when creating an asset.
        """
        serializer.save(tenant=self.request.tenant)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Generate a signed URL for downloading the asset.
        """
        asset = self.get_object()
        
        # In a real implementation, this would generate a signed URL for the asset
        # using something like S3's presigned URLs or MinIO's presigned URLs
        # For now, we'll just return a placeholder URL
        
        # Example implementation:
        # from minio import Minio
        # client = Minio(
        #     "minio-server:9000",
        #     access_key="minioadmin",
        #     secret_key="minioadmin",
        #     secure=False
        # )
        # url = client.presigned_get_object(
        #     "assets",
        #     asset.file_path,
        #     expires=timedelta(minutes=30)
        # )
        
        # Placeholder implementation
        expires = timezone.now() + timedelta(minutes=30)
        download_url = f"https://storage.talemo.app/{request.tenant.schema_name}/{asset.file_path}"
        
        serializer = self.get_serializer({
            'download_url': download_url,
            'expires_at': expires
        })
        return Response(serializer.data)


class AssetUsageViewSet(viewsets.ViewSet):
    """
    API endpoint for tenant storage usage statistics.
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """
        Get storage usage statistics for the current tenant.
        """
        # Get total number of assets and total size
        assets = Asset.objects.filter(tenant=request.tenant)
        total_assets = assets.count()
        total_size = assets.aggregate(total=Sum('file_size'))['total'] or 0
        
        # Get breakdown by type
        by_type = {}
        for asset_type in ['image', 'audio', 'user_audio']:
            type_assets = assets.filter(type=asset_type)
            type_count = type_assets.count()
            type_size = type_assets.aggregate(total=Sum('file_size'))['total'] or 0
            by_type[asset_type] = {
                'count': type_count,
                'size': type_size
            }
        
        data = {
            'total_assets': total_assets,
            'total_size': total_size,
            'by_type': by_type
        }
        
        serializer = AssetUsageSerializer(data)
        return Response(serializer.data)