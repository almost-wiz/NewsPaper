# Generated by Django 3.2 on 2021-07-06 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPaperApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='postcategory',
            options={'verbose_name': 'Post category', 'verbose_name_plural': 'Post categories'},
        ),
    ]
