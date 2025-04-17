from django.db import models


# Create your models here.
class MyEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
