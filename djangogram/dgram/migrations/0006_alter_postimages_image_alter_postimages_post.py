# Generated by Django 4.1.1 on 2022-10-19 19:18

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dgram', '0005_post_dislikes_post_likes_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimages',
            name='image',
            field=cloudinary.models.CloudinaryField(default='something', max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postimages',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='dgram.post'),
        ),
    ]
