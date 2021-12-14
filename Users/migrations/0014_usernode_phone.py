# Generated by Django 3.2.9 on 2021-11-27 09:22

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0013_auto_20211127_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernode',
            name='Phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]