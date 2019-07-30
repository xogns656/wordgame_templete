# Generated by Django 2.2.3 on 2019-07-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('uid', models.TextField()),
                ('chain_easy', models.IntegerField(default=0)),
                ('chain_hard', models.IntegerField(default=0)),
                ('init_easy', models.IntegerField(default=0)),
                ('init_hard', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('word_type', models.TextField()),
                ('word_length', models.IntegerField(default=0)),
                ('first_sound', models.TextField()),
                ('last_sound', models.TextField()),
                ('simple', models.BooleanField(default=False)),
                ('pos', models.TextField()),
                ('noun', models.BooleanField(default=False)),
                ('very_simple', models.BooleanField(default=False)),
                ('consonants', models.TextField()),
            ],
        ),
    ]
