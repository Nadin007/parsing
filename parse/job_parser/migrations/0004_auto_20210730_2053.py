# Generated by Django 3.2.5 on 2021-07-30 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_parser', '0003_auto_20210730_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='c_url',
            field=models.URLField(blank=True, db_index=True, max_length=1000, unique=True, verbose_name='Company URL'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='informLink',
            field=models.URLField(blank=True, db_index=True, max_length=1000, unique=True, verbose_name='additional information'),
        ),
    ]
