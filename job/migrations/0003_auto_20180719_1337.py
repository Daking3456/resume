# Generated by Django 2.0.7 on 2018-07-19 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20180719_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
