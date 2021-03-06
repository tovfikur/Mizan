# Generated by Django 3.2.9 on 2021-12-06 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Users', '0020_userrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saledetails',
            name='AgentName',
        ),
        migrations.AddField(
            model_name='debitcategory',
            name='Creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='debitcategory',
            name='User',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usernode',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
