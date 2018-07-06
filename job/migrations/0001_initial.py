# Generated by Django 2.0.7 on 2018-07-06 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('zip_code', models.CharField(max_length=200, null=True)),
                ('address1', models.CharField(max_length=200, null=True)),
                ('address2', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'addresses',
                'db_table': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=300, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'companies',
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('responsibilities', models.TextField(blank=True, null=True)),
                ('qualification', models.TextField(blank=True, null=True)),
                ('education', models.CharField(blank=True, max_length=500, null=True)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('no_opening', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('slug', models.SlugField(unique=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'jobs',
                'db_table': 'job',
            },
        ),
    ]
