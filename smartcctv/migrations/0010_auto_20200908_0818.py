# Generated by Django 3.0.3 on 2020-09-08 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcctv', '0009_auto_20200908_0808'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeopleCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField()),
                ('up', models.IntegerField()),
                ('down', models.IntegerField()),
                ('date', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'people_count',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='SmartcctvPeople',
        ),
    ]