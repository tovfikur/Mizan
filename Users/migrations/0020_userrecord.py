# Generated by Django 3.2.9 on 2021-12-05 11:53

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0019_auto_20211128_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(blank=True, max_length=30, null=True)),
                ('LastName', models.CharField(blank=True, max_length=30, null=True)),
                ('EmailAddress', models.EmailField(blank=True, max_length=254, null=True)),
                ('Active', models.BooleanField(default=False)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('pid', models.IntegerField(blank=True, default=None, null=True)),
                ('Address', models.TextField(blank=True, null=True)),
                ('Phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('Position', models.SmallIntegerField(blank=True, choices=[('Owner', 'Owner'), ('Admin', 'Admin'), ('Employee', 'Employee')], null=True)),
            ],
        ),
    ]
