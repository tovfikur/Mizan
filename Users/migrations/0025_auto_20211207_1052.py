# Generated by Django 3.2.9 on 2021-12-07 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0024_auto_20211206_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernode',
            name='CreditCategory',
            field=models.ManyToManyField(blank=True, null=True, to='Users.CreditCategory'),
        ),
        migrations.AddField(
            model_name='usernode',
            name='DebitCategory',
            field=models.ManyToManyField(blank=True, null=True, to='Users.DebitCategory'),
        ),
    ]
