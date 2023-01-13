from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(default='profiles/avatars/default.jpg', upload_to='profiles/avatars')
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #    super().save(*args, **kwargs)

    #    img = Image.open(self.image.path)

    #    if img.height > 300 or img.width > 300:
    #        output_size = (300, 300)
    #        img.thumbnail(output_size)
    #        img.save(self.image.name)
