# Generated by Django 5.0.2 on 2025-07-02 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_committeemember_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrepreneur',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entrepreneur',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
