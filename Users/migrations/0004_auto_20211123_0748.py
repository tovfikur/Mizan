# Generated by Django 3.2.9 on 2021-11-23 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_rename_usertree_usernode'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernode',
            name='Address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usernode',
            name='Name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='usernode',
            name='Position',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Owner'), (2, 'Admin'), (3, 'Employee')], null=True),
        ),
    ]
