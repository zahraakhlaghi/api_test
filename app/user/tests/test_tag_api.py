from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Tag,Post
from ..serializers import TagSerializer

from rest_framework.test import APIClient
from rest_framework import status

TAG_URL = reverse('user:tag-list')


class TagApiTests(TestCase):
    """Test unauthenticated tag API access"""

    def setUp(self):
        self.client = APIClient()
        
    def test_tag_invalid(self):
        """Test creatinga  tag invalid"""
        payload = {
            'name':''
        }
        res = self.client.post(TAG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid_tag_success(self):
        """Test creating tag with valid payload is successful"""
        payload = {
            'name': 'Test name'
        }
        res = self.client.post(TAG_URL, payload)
        exists = Tag.objects.filter(name=payload['name']).exists()

        self.assertTrue(exists)    

    def test_retrieve_tag(self):
        """Test retrieving a list of tag"""
        Tag.objects.create(name='tag1')
        Tag.objects.create(name='tag2')

        res = self.client.get(TAG_URL)

        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)    

    