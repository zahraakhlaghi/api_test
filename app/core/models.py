from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status =models.BooleanField(default=1)
    """status 0->inactive 1->active"""
    cdt = models.DateTimeField(auto_now=True)
    udt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Tag(models.Model): 

    name = models.CharField(max_length=255)
    status =models.BooleanField(default=1)
    cdt = models.DateTimeField(auto_now=True)
    udt = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    status =models.BooleanField(default=1)
    cdt = models.DateTimeField(auto_now=True)
    udt = models.DateTimeField(auto_now=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts',
                                  blank=True)

    def __str__(self): 
       return self.title                                 