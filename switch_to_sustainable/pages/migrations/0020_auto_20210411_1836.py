# Generated by Django 3.1.2 on 2021-04-11 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_item_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
