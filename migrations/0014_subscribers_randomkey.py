# Generated by Django 2.1.4 on 2019-01-31 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_subscribers_confirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribers',
            name='randomkey',
            field=models.CharField(default=1234, help_text='Рандомный ключ', max_length=100),
            preserve_default=False,
        ),
    ]