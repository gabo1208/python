# Generated by Django 5.1.4 on 2025-01-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField(max_length=200)),
                ('authors_option', models.CharField(max_length=200)),
                ('authorId', models.IntegerField(default=0)),
            ],
        ),
    ]
