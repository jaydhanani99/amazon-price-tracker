from rest_framework import viewsets, mixins, pagination, status
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import filters

from core.models import Meme
from meme import serializers

class MemePagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_response(self, data):
        return Response({
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current': self.page.number,
            'data': data
        })

class MemeViewSet(viewsets.ModelViewSet):
    """Manage memes in database"""
    queryset = Meme.objects.all().order_by('-id')

    serializer_class = serializers.MemeSerializer
    pagination_class = MemePagination

    filter_backends = [filters.SearchFilter]
    # global full text search for caption and name
    search_fields = ['caption', 'name']

    # def get_queryset(self):
    #     queryset = self.queryset

    #     caption = self.request.query_params.get('caption', None)
    #     if caption is not None:
    #         queryset = queryset.filter(caption__contains=caption)

    #     name = self.request.query_params.get('name', None)
    #     if name is not None:
    #         queryset = queryset.filter(name__contains=name)

    #     return queryset


    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = serializers.MemeSerializerWithoutName

        return serializer_class

    # def perform_create(self, serializer):
    #     """Create a new meme"""
    #     serializer.save()

    def create(self, request, *args, **kwargs):
        # Override create method to prevent duplicate object creation
        serializer = serializers.MemeSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        caption = serializer.validated_data['caption']
        url = serializer.validated_data['url']

        if Meme.objects.filter(name=name, caption=caption, url=url).exists():
            return Response(status=status.HTTP_409_CONFLICT)
            
        # Meme.objects.create(name=name, caption=caption, url=url)
        meme = serializer.save()
        response_serialized_meme = serializers.MemeSerializer(meme).data
        return Response(response_serialized_meme, status=status.HTTP_201_CREATED)