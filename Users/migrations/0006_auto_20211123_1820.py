# Generated by Django 3.2.9 on 2021-11-23 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_rename_pid_usernode_cid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernode',
            name='CID',
        ),
        migrations.AddField(
            model_name='usernode',
            name='CID',
            field=models.ManyToManyField(blank=True, null=True, related_name='_Users_usernode_CID_+', to='Users.UserNode'),
        ),
    ]