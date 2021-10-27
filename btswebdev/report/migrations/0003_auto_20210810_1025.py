# Generated by Django 3.2.2 on 2021-08-10 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_report_report_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('subject_name', models.TextField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='report_end_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='report',
            name='report_start_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]