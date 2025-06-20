# Generated by Django 5.2.3 on 2025-06-18 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='news_resources/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.TextField()),
                ('url', models.URLField()),
                ('matched_on', models.DateTimeField(auto_now_add=True)),
                ('triggered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent2_news.newsresource')),
            ],
        ),
    ]
