# Generated by Django 5.1.6 on 2025-02-15 10:15

import django.core.validators
import django.db.models.deletion
import enterpoll.custom_validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, validators=[enterpoll.custom_validators.forbidden_words], verbose_name='Заголовок')),
                ('description', models.CharField(blank=True, max_length=100, null=True, validators=[enterpoll.custom_validators.forbidden_words], verbose_name='Описание')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100, validators=[enterpoll.custom_validators.forbidden_words], verbose_name='Текст')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterpoll.poll')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100, validators=[enterpoll.custom_validators.forbidden_words], verbose_name='')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterpoll.poll')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created', models.DateTimeField(auto_now=True)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterpoll.poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterpoll.choice')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterpoll.poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='poll',
            constraint=models.UniqueConstraint(fields=('title', 'user'), name='unique_poll'),
        ),
        migrations.AddConstraint(
            model_name='choice',
            constraint=models.UniqueConstraint(fields=('poll', 'text'), name='unique_choice'),
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(fields=('user', 'poll'), name='unique_rating'),
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('user', 'poll'), name='unique_vote'),
        ),
    ]
