# Generated by Django 3.2.2 on 2021-08-10 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20210810_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report.subject'),
        ),
    ]
