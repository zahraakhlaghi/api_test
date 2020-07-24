from rest_framework import serializers

from core.models import Tag,Category,Post


class  CategorySerializer(serializers.ModelSerializer): 
    """Serializer for category objects"""
    class Meta:
        model = Category
        fields = (
            'id','name','status','cdt','udt'
            )
        read_only_fields = ('id',)

class  TagSerializer(serializers.ModelSerializer): 
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        fields = (
            'id','name','cdt','udt','status'
            )
        read_only_fields = ('id',)

class PostSerializer(serializers.ModelSerializer):      
    """Serializer for post objects"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    class Meta:
        model = Post
        fields = (
            'id','title','content','category_id','status',
            'cdt','udt'
            )
        read_only_fields = ('id',)

class PostDetailSerializer(PostSerializer):
    """Serialize a post detail"""
    tags = TagSerializer(many=True, read_only=True)

     
    


    