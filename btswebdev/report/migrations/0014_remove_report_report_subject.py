# Generated by Django 3.2.2 on 2021-10-18 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0013_alter_report_report_additional_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='report_subject',
        ),
    ]
