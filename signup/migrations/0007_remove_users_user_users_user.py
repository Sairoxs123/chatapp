# Generated by Django 4.1.7 on 2023-09-19 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0006_users_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user',
        ),
        migrations.AddField(
            model_name='users',
            name='user',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='signup.messages'),
            preserve_default=False,
        ),
    ]
