# Generated by Django 5.0.7 on 2024-08-05 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aayo', '0006_cafe_logoimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='name_eng',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
