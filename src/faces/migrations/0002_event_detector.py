# Generated by Django 2.2.1 on 2019-05-14 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='detector',
            field=models.CharField(default='default', max_length=50, verbose_name='camera detector'),
            preserve_default=False,
        ),
    ]
