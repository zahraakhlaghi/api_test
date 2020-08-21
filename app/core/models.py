from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status =models.BooleanField(default=1)
    """status 0->inactive 1->active"""
    cdt = models.DateTimeField(auto_now=True)
    udt = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def soft_del(self):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.name


class Tag(models.Model): 

    name = models.CharField(max_length=255)
    status =models.BooleanField(default=1)
    cdt = models.DateTimeField(auto_now=True)
    udt = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def soft_del(self):
        self.deleted = True
        self.save()
 
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
    deleted = models.BooleanField(default=False)

    def soft_del_category(self):
        self.deleted = True
        for b in Category.related_Bs.all():
            b.soft_del_B()

        self.save()

    def soft_del_tag(self):
        self.deleted = True
        for b in Tag.related_Bs.all():
            b.soft_del_B()

        self.save()


    def __str__(self): 
       return self.title                                 