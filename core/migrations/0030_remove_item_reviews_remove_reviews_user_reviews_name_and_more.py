# Generated by Django 4.1.4 on 2023-01-13 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_reviews_item_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='reviews',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='user',
        ),
        migrations.AddField(
            model_name='reviews',
            name='name',
            field=models.CharField(default='Unknown', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviews',
            name='showOnItem',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reviews',
            name='stars',
            field=models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], default=5, max_length=2),
        ),
        migrations.CreateModel(
            name='ReviewAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.item')),
                ('reviews', models.ManyToManyField(to='core.reviews')),
            ],
        ),
    ]
