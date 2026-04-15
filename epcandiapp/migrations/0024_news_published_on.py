from datetime import date

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epcandiapp', '0023_banneradvertisement'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='published_on',
            field=models.DateField(default=date.today),
        ),
    ]