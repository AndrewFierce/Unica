# Generated by Django 2.1.4 on 2019-01-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20190116_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='posts/%Y/%m/%d'),
        ),
    ]
