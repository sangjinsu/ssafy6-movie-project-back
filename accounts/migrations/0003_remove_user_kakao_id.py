# Generated by Django 3.2.3 on 2021-11-29 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_kakao_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='kakao_id',
        ),
    ]