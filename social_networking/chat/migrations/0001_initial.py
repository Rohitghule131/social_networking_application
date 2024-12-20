# Generated by Django 5.0.6 on 2024-10-21 09:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('chat_room', models.CharField(max_length=200)),
                ('users', models.ManyToManyField(related_name='chat_between_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('messages', models.TextField()),
                ('link', models.URLField(null=True)),
                ('link_type', models.CharField(choices=[('IMAGE', 'IMAGE'), ('PDF', 'PDF')], max_length=50, null=True)),
                ('chat_room_connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatconnection')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]