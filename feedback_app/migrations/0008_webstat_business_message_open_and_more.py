# Generated by Django 4.1.7 on 2023-04-10 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_app', '0007_webstat'),
    ]

    operations = [
        migrations.AddField(
            model_name='webstat',
            name='business_message_open',
            field=models.IntegerField(default=0, editable=False, verbose_name='Number of business messsage opens'),
        ),
        migrations.AddField(
            model_name='webstat',
            name='business_message_post',
            field=models.IntegerField(default=0, editable=False, verbose_name='Number of business messsage posts'),
        ),
        migrations.AddField(
            model_name='webstat',
            name='personal_message_open',
            field=models.IntegerField(default=0, editable=False, verbose_name='Number of personal messsage opens'),
        ),
        migrations.AddField(
            model_name='webstat',
            name='personal_message_post',
            field=models.IntegerField(default=0, editable=False, verbose_name='Number of personal messsage posts'),
        ),
    ]