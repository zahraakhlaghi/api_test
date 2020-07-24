from rest_framework import viewsets,generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag,Post,Category
from . import serializers
  
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = '__all__'

    @action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny])

    def posts(self, request, pk=None):
        category = Category.objects.get(id=pk)
        post = Post.objects.filter(category_id=category)
        serializer = serializers.PostSerializer(post, many=True)
        return Response(serializer.data)
 
class TagViewSet(viewsets.ModelViewSet):
    """manage tag in tha database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = '__all__'

    @action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny])

    def posts(self, request, pk=None):
        tag = Tag.objects.get(id=pk)
        post = Post.objects.filter(tag=tag)
        serializer = serializers.TagSerializer(post, many=True)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    """Manage post in the database"""
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.AllowAny,)

    search_fields = ('title','content')
    ordering_fields = ('title')
    @action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny])   

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        tags = self.request.query_params.get('tags')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.PostDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new post"""
        serializer.save()

    




