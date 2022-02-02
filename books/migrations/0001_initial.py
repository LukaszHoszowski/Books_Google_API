# Generated by Django 4.0.1 on 2022-02-02 00:21

import books.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Author name', max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(help_text='Language', max_length=2)),
            ],
            options={
                'ordering': ['lang'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title', max_length=1000)),
                ('published_date', models.SmallIntegerField(blank=True, help_text='Publish year', null=True, validators=[books.validators.validate_year])),
                ('isbn', models.CharField(blank=True, help_text='ISBN', max_length=13, null=True, validators=[books.validators.validate_isbn])),
                ('page_count', models.PositiveIntegerField(blank=True, help_text='Page count', null=True)),
                ('cover_link', models.URLField(blank=True, help_text='Link to cover of the book', null=True)),
                ('author', models.ManyToManyField(blank=True, help_text='Authors list', related_name='authors', to='books.Author')),
                ('language', models.ForeignKey(help_text='Book language', on_delete=django.db.models.deletion.DO_NOTHING, related_name='languages', to='books.language')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]