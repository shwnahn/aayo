# Generated by Django 5.0.7 on 2024-08-03 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aayo', '0004_cafe_remove_room_creator_menuitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestorder',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='room',
            name='created_at',
        ),
    ]