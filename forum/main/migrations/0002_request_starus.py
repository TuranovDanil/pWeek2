# Generated by Django 3.2.16 on 2022-11-14 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='starus',
            field=models.CharField(choices=[('new', 'новая'), ('work', 'принято в работу'), ('completed', 'выполнено')], default='new', max_length=60, verbose_name='Статус'),
        ),
    ]
