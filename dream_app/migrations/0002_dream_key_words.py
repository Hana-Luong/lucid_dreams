# Generated by Django 2.2 on 2019-12-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dream_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dream',
            name='key_words',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
    ]
