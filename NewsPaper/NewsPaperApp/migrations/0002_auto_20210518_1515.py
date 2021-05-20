# Generated by Django 3.2 on 2021-05-18 12:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPaperApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='rating',
            field=models.FloatField(default=0.0, max_length=10),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.FloatField(default=0.0, max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.FloatField(default=0.0, max_length=10),
        ),
    ]
