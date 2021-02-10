# Generated by Django 3.0.6 on 2021-02-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='post/')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100)),
                ('intro', models.TextField()),
                ('body', models.TextField()),
                ('pub_date', models.DateField()),
                ('added', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('custom_css', models.TextField(blank=True)),
                ('custom_javascript', models.TextField(blank=True)),
            ],
        ),
    ]
