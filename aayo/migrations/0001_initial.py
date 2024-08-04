# Generated by Django 5.0.7 on 2024-07-29 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('creator', models.CharField(max_length=50)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('cafe', models.CharField(max_length=20)),
                ('unique_id', models.CharField(max_length=8, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
