# Generated by Django 4.1.4 on 2023-01-11 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(height_field='500', unique=True, upload_to='media/uploads/', width_field='500'),
        ),
    ]
