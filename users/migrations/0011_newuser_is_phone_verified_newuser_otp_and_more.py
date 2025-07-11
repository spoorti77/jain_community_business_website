# Generated by Django 5.0.2 on 2025-07-03 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_familymember_head_of_family'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='is_phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newuser',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='newuser',
            name='otp_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
