# Generated by Django 4.1.1 on 2022-10-05 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgram', '0002_remove_post_content_postimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_pics'),
        ),
    ]
