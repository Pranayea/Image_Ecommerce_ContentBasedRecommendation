# Generated by Django 3.0.8 on 2021-04-18 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210215_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fund',
            field=models.IntegerField(default=0),
        ),
    ]
