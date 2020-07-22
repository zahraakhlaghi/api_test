from django.test import TestCase
from django.contrib.auth import get_user_model
from .. import models


class ModelTests(TestCase):
    def test_category_str(self):
        category1 = models.Category.objects.create(name='test category')

        self.assertEqual(str(category1), category1.name)

    def test_tag_str(self):
        tag1 = models.Tag.objects.create(name="test tag")

        self.assertEqual(str(tag1), tag1.name)          

    def test_post_str(self):
        post1 = models.Post.objects.create(
            title="test",
            category_id=models.Category.objects.create(name='test category'),
            content='test content'
        )
        self.assertEqual(str(post1), post1.title)

  
