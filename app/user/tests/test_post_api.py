from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Tag,Post,Category
from ..serializers import CategorySerializer,PostSerializer,PostDetailSerializer

from rest_framework.test import APIClient
from rest_framework import status

POST_URL = reverse('user:post-list')


def detail_url(post_id):
    """Return post detail URL"""
    return reverse('user:post-list', args=[post_id])

def sample_tag(name='test tag'):
    return Tag.objects.create(name=name)

def sample_category(name='test category'):
   """create and return a cample category"""
   return Category.objects.create(name=name)

def sample_post(category, **params):
    """Create and return sample post"""
    defaults = {
        'title': 'test Title',
        'content': 'test content',
    }
    defaults.update(params)

    return Post.objects.create(category_id=category, **defaults)

class PostApiTests(TestCase):
    """Test the authorized user post API"""
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_post(self):
        """Test retrieving post"""
        category = sample_category(name='test')
        sample_post(category)
        sample_post(category)
        res = self.client.get(POST_URL)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK) 

    def test_create_basic_post(self):
        """Test creating post"""
        category=sample_category()
        payload = {
            'title': 'title 1',
            'content':'test content',
            'category_id':category.id
        }
        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key=='category_id':
                self.assertEqual(payload[key], getattr(post, key).id)
            else:
                self.assertEqual(payload[key], getattr(post, key))        


    def test_create_post_with_tags(self):
        """Test creating a post with tags"""
        tag1 = sample_tag(name='sample tag 1')
        tag2 = sample_tag(name='sample tag 2')
        category=sample_category()
        payload = {
            'title': 'title 1',
            'content':'test content',
            'category_id':category.id,
            'tags': [tag1.id, tag2.id],
        }
        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        posts = Post.objects.get(id=res.data['id'])
        tags = posts.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_partial_update_post(self):
        """*Test updating a post with patch"""
        post = sample_post(sample_category())
        post.tags.add(sample_tag(name='tag1'))
        new_tag = sample_tag(name='tag2')
        category=sample_category(name='sample category')

        payload = {
            'title': 'new title',
            'content':'test content',
            'category_id':category.id,
            'tags': [new_tag.id],
        }
        url = detail_url(post.id)
        self.client.patch(url, payload)

        post.refresh_from_db()
        self.assertEqual(post.title, payload['title'])
        tags = post.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_post(self):
        """Test updating a post with put"""
        post = sample_post(sample_category())
        post.tags.add(sample_tag(name='tag1'))
        category=sample_category(name='sample category')
        payload = {
            'title': 'title 1',
            'content':'test content',
            'category_id':category.id,
        }
        url = detail_url(post.id)
        self.client.put(url, payload)

        post.refresh_from_db()


        tags = post.tags.all()
        self.assertEqual(len(tags), 0)  

        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.content, payload['content'])
        

    def test_filter_post_by_tags(self):
        """Test returning post with specific tags"""
        post1 = sample_post(sample_category(name='category1'))
        post2 = sample_post(sample_category(name='category2'))
        tag1 = sample_tag(name='test tag1')
        tag2 = sample_tag(name='test tag2')
        post1.tags.add(tag1)
        post2.tags.add(tag2)
        post3 = sample_post(sample_category(name='category3'))

        res = self.client.get(
            POST_URL,
            {'tags': f'{tag1.id},{tag2.id}'}
        )

        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)
        serializer3 = PostSerializer(post3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)          
     
