# Generated by Django 5.0.6 on 2024-11-04 05:14

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='send_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chatconnection',
            name='chat_room',
            field=models.CharField(default=uuid.UUID('315a7abd-6ea3-4927-a438-b35175101ebb'), max_length=200),
        ),
    ]
