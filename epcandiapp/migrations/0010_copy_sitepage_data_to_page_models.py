from django.db import migrations


def copy_sitepage_data(apps, schema_editor):
    SitePage = apps.get_model("epcandiapp", "SitePage")
    AboutPage = apps.get_model("epcandiapp", "AboutPage")
    TendersPage = apps.get_model("epcandiapp", "TendersPage")
    CatalogsPage = apps.get_model("epcandiapp", "CatalogsPage")
    DisclaimerPage = apps.get_model("epcandiapp", "DisclaimerPage")
    PrivacyPage = apps.get_model("epcandiapp", "PrivacyPage")
    JobsPage = apps.get_model("epcandiapp", "JobsPage")
    AdvertisePage = apps.get_model("epcandiapp", "AdvertisePage")
    MediaKitPage = apps.get_model("epcandiapp", "MediaKitPage")
    ShoppingCartPage = apps.get_model("epcandiapp", "ShoppingCartPage")

    slug_map = {
        "about": AboutPage,
        "tenders": TendersPage,
        "catalogs": CatalogsPage,
        "disclaimer": DisclaimerPage,
        "privacy": PrivacyPage,
        "jobs": JobsPage,
        "advertise": AdvertisePage,
        "media-kit": MediaKitPage,
        "shopping-cart": ShoppingCartPage,
    }

    for source in SitePage.objects.all():
        target_model = slug_map.get(source.slug)
        if not target_model:
            continue
        target_model.objects.update_or_create(
            id=1,
            defaults={
                "title": source.title,
                "heading": source.heading,
                "content": source.content,
                "is_published": source.is_published,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("epcandiapp", "0009_aboutpage_advertisepage_catalogspage_disclaimerpage_and_more"),
    ]

    operations = [
        migrations.RunPython(copy_sitepage_data, migrations.RunPython.noop),
    ]
