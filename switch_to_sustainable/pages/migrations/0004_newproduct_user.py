# Generated by Django 3.1.2 on 2021-04-03 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20210401_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]