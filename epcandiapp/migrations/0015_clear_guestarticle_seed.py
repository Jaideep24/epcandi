from django.db import migrations


def clear_guest_articles(apps, schema_editor):
    GuestArticle = apps.get_model("epcandiapp", "GuestArticle")
    GuestArticle.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("epcandiapp", "0014_guestarticle"),
    ]

    operations = [
        migrations.RunPython(clear_guest_articles, migrations.RunPython.noop),
    ]
