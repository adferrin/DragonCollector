# Generated by Django 3.1 on 2020-09-10 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_feeding'),
    ]

    operations = [
        migrations.AddField(
            model_name='dragon',
            name='toys',
            field=models.ManyToManyField(to='main_app.Toy'),
        ),
    ]
