# Generated by Django 5.0.7 on 2024-08-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aayo', '0011_menuitem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
