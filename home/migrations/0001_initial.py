# Generated by Django 4.2.9 on 2024-05-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('inductedDate', models.IntegerField(blank=True, null=True)),
                ('numServiceHours', models.IntegerField(default=0)),
            ],
        ),
    ]
