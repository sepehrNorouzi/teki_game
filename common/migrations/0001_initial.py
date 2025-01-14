# Generated by Django 5.1 on 2024-08-27 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommonConfigurationJsonConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('config', models.JSONField(verbose_name='Config')),
            ],
            options={
                'verbose_name': 'Common Json Config',
                'verbose_name_plural': 'Common Json Configs',
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('app_name', models.CharField(default='teki_game', max_length=255, verbose_name='App Name')),
                ('maintenance_mode', models.BooleanField(default=False, verbose_name='Maintenance mode')),
                ('config', models.ManyToManyField(blank=True, null=True, to='common.commonconfigurationjsonconfig', verbose_name='Config')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
            },
        ),
    ]
