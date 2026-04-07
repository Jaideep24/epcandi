from django.db import migrations, models


def copy_articles_to_guest_articles(apps, schema_editor):
    Articles = apps.get_model("epcandiapp", "Articles")
    GuestArticle = apps.get_model("epcandiapp", "GuestArticle")

    for article in Articles.objects.all().order_by("id"):
        GuestArticle.objects.create(heading=article.heading, article=article.article)


def reverse_copy_articles_to_guest_articles(apps, schema_editor):
    GuestArticle = apps.get_model("epcandiapp", "GuestArticle")
    GuestArticle.objects.all().delete()


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
        migrations.RunPython(copy_articles_to_guest_articles, reverse_copy_articles_to_guest_articles),
    ]
