# Generated by Django 3.0.5 on 2020-05-29 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_stock',
            options={'verbose_name_plural': '自选股'},
        ),
    ]