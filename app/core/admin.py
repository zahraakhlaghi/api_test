from django.contrib import admin
from core import models

admin.site.register(models.Category)
admin.site.register(models.Post)
admin.site.register(models.Tag)