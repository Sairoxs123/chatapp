# Generated by Django 4.1.7 on 2023-09-19 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0005_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='user',
            field=models.ManyToManyField(blank=True, to='signup.messages'),
        ),
    ]
