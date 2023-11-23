# Generated by Django 4.2.7 on 2023-11-22 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('legal_services', '0004_query_contacted_before'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('first_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread_first_user', to=settings.AUTH_USER_MODEL)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legal_services.query')),
                ('second_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread_second_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('first_user', 'second_user', 'query')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.messagethread')),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
    ]
