from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("epcandiapp", "0015_clear_guestarticle_seed"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Articles",
            new_name="Focus",
        ),
        migrations.RenameModel(
            old_name="Equipment_News",
            new_name="EquipmentNews",
        ),
        migrations.RenameField(
            model_name="interview",
            old_name="Interview",
            new_name="interview",
        ),
        migrations.AlterModelOptions(
            name="focus",
            options={"verbose_name": "Focus", "verbose_name_plural": "Focus"},
        ),
    ]
