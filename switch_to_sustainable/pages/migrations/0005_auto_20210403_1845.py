# Generated by Django 3.1.2 on 2021-04-03 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_newproduct_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='text',
            new_name='name',
        ),
    ]
