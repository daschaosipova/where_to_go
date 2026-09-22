from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0004_alter_place_lat_alter_place_lng"),
    ]

    operations = [
        migrations.RenameField(
            model_name="place",
            old_name="description_short",
            new_name="short_description",
        ),
        migrations.RenameField(
            model_name="place",
            old_name="description_long",
            new_name="long_description",
        ),
    ]