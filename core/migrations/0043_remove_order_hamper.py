# Generated by Django 4.1.4 on 2023-01-25 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_images_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='hamper',
        ),
    ]
