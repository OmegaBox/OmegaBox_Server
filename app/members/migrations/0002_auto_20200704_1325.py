# Generated by Django 2.2.13 on 2020-07-04 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='genre',
            field=models.ManyToManyField(related_name='profiles', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='profile',
            name='member',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]