# Generated by Django 3.2.3 on 2021-11-29 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_kakao_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kakao_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
