# Generated by Django 3.2.2 on 2021-08-10 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_report_report_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='report_start_date',
            field=models.DateTimeField(),
        ),
    ]
