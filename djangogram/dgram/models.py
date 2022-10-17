from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django_extensions.db.fields import AutoSlugField
from PIL import Image

class Post(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    slug = AutoSlugField(populate_from='title', unique=True)

    def slugify_function(self, content):
        posts_count = Post.objects.count()
        return content.replace('_', '-').lower() + str(posts_count)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class PostImages(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pics', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 1080 or img.width > 1080:
            output_size = (1080, 1080)
            img.thumbnail(output_size)
            img.save(self.image.path)






