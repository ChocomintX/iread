# Generated by Django 4.0.3 on 2023-03-07 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_manga_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='status',
            field=models.CharField(max_length=200, verbose_name='状态'),
        ),
    ]
