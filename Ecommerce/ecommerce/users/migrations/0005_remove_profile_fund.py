# Generated by Django 3.0.8 on 2021-05-01 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='fund',
        ),
    ]