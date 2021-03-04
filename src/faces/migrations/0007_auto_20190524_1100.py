# Generated by Django 2.2.1 on 2019-05-24 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faces', '0006_auto_20190515_1342'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'событие', 'verbose_name_plural': 'события'},
        ),
        migrations.AlterModelOptions(
            name='eventnotification',
            options={'verbose_name': 'уведомление о событии', 'verbose_name_plural': 'уведомления о событиях'},
        ),
        migrations.AddField(
            model_name='event',
            name='age',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='age'),
        ),
        migrations.AddField(
            model_name='event',
            name='gender',
            field=models.CharField(blank=True, max_length=10, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='event',
            name='camera',
            field=models.UUIDField(verbose_name='ID камеры'),
        ),
        migrations.AlterField(
            model_name='event',
            name='detector',
            field=models.CharField(max_length=50, verbose_name='детектор камеры'),
        ),
        migrations.AlterField(
            model_name='eventnotification',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faces.Event', verbose_name='событие'),
        ),
    ]
