from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("epcandiapp", "0017_shoppingcart_squarefoot_alter_aboutpage_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="events",
            name="banner",
            field=models.FileField(blank=True, null=True, upload_to="event_banners/"),
        ),
    ]
