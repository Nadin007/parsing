# Generated by Django 3.2.5 on 2021-07-30 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_parser', '0005_auto_20210730_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='c_url',
            field=models.URLField(blank=True, db_index=True, max_length=1000, null=True, verbose_name='Company URL'),
        ),
    ]