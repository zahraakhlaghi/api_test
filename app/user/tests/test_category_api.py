from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Post,Category,Post
from ..serializers import CategorySerializer

from rest_framework.test import APIClient
from rest_framework import status

CATEGORY_URL = reverse('user:category-list')


class PrivateRecipeApiTests(TestCase):
    """Test unauthenticated category API access"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_category(self):
        """Test retrieving a list of category"""
        Category.objects.create(name='category1')
        Category.objects.create(name='category2')

        res = self.client.get(CATEGORY_URL)

        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_valid_category_success(self):
        """Test creating category with valid payload is successful"""
        payload = {
            'name': 'Test name'
        }
        res = self.client.post(CATEGORY_URL, payload)
        exists = Category.objects.filter(name=payload['name']).exists()

        self.assertTrue(exists)

    def test_category_invalid(self):
        """Test creatinga  category invalid"""
        payload = {
            'name':''
        }
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_category_exists(self):
        """test category exist"""
        payload = {'name': 'test name'}
        self.client.post(CATEGORY_URL, payload)

        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
   
        
