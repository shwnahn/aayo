# Generated by Django 5.0.7 on 2024-08-06 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aayo', '0013_guestorder_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestorder',
            name='menu_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aayo.menuitem'),
        ),
    ]