# Generated by Django 4.1.4 on 2023-02-18 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_order_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.SlugField(blank=True, default=''),
        ),
    ]
