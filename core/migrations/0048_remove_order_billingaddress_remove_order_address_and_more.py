# Generated by Django 4.1.4 on 2023-01-26 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_rename_appartment_address_billingaddress_apartment_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='BillingAddress',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_mode',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
        migrations.RemoveField(
            model_name='order',
            name='zip_code',
        ),
    ]
