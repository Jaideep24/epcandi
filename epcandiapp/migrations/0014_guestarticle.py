from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("epcandiapp", "0013_normalize_pagecontent_titles"),
    ]

    operations = [
        migrations.CreateModel(
            name="GuestArticle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("heading", models.CharField(max_length=200)),
                ("article", models.TextField()),
            ],
            options={
                "verbose_name": "Guest Article",
                "verbose_name_plural": "Guest Articles",
            },
        ),
    ]
