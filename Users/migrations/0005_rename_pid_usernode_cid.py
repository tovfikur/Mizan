# Generated by Django 3.2.9 on 2021-11-23 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_auto_20211123_0748'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usernode',
            old_name='PID',
            new_name='CID',
        ),
    ]
