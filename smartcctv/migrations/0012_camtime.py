# Generated by Django 3.0.3 on 2020-09-29 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcctv', '0011_camera'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camtime',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('detection_start', models.IntegerField(blank=True, null=True)),
                ('detection_end', models.IntegerField(blank=True, null=True)),
                ('peoplecount_start', models.IntegerField(blank=True, null=True)),
                ('peoplecount_end', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'camTime',
                'managed': False,
            },
        ),
    ]
