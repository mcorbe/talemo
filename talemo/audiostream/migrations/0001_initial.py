# Generated by Django 5.2.4 on 2025-07-17 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioSession',
            fields=[
                ('session_id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=12)),
                ('playlist_rel_url', models.CharField(blank=True, max_length=200)),
                ('error_message', models.TextField(blank=True)),
            ],
        ),
    ]
