# Generated by Django 5.1.3 on 2025-01-13 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_downvotes_post_upvotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='upvotes',
        ),
    ]
