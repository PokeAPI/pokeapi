from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon_v2", "0033_itemprice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemonevolution",
            name="time_of_day",
            field=models.CharField(blank=True, default="", max_length=10),
        ),
        migrations.RemoveField(
            model_name="item",
            name="cost",
        ),
    ]
