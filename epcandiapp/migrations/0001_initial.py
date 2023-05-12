# Generated by Django 2.2.5 on 2023-05-02 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('A', 'Aviation'), ('C', 'Cement'), ('I', 'Infrastructure'), ('IT', 'IT and Telecom'), ('O', 'Oil and Gas'), ('P', 'Power'), ('R', 'Real Estate')], max_length=200)),
                ('news', models.CharField(max_length=2000)),
            ],
        ),
    ]
