# Generated by Django 2.2.14 on 2020-07-16 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_member_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='unique_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]