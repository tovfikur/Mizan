# Generated by Django 3.2.9 on 2021-12-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0023_auto_20211206_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcategory',
            name='Title',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='debitcategory',
            name='Title',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
    ]
