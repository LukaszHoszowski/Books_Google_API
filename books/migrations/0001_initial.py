# Generated by Django 4.0.1 on 2022-01-29 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('published_date', models.DateTimeField()),
                ('isbn', models.CharField(max_length=13)),
                ('page_count', models.IntegerField(help_text='Page count')),
                ('cover_link', models.CharField(max_length=300)),
                ('language', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
