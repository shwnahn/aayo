# Generated by Django 5.0.7 on 2024-08-05 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aayo', '0007_cafe_name_eng'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafe',
            name='logoimage',
        ),
    ]