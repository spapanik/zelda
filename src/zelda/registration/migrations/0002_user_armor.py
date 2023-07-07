from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("armor", "0001_initial"),
        ("registration", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="armor",
            field=models.ManyToManyField(through="armor.UserArmor", to="armor.armor"),
        ),
    ]
