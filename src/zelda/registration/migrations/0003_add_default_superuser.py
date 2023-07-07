from django.apps.registry import Apps
from django.contrib.auth.hashers import make_password
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

DEFAULT_EMAIL = "link@hyrule.gov"
DEFAULT_PASSWORD = "zelda"  # noqa: S105


def create_initial_superuser(
    apps: Apps, _schema_editor: BaseDatabaseSchemaEditor
) -> None:
    User = apps.get_model("registration", "User")  # noqa: N806

    user, created = User.objects.get_or_create(email=DEFAULT_EMAIL)
    if created:
        user.password = make_password(DEFAULT_PASSWORD)
        user.is_superuser = True
        user.is_staff = True
        user.save()


def drop_initial_superuser(
    apps: Apps, _schema_editor: BaseDatabaseSchemaEditor
) -> None:
    User = apps.get_model("registration", "User")  # noqa: N806

    User.objects.filter(email=DEFAULT_EMAIL).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("registration", "0002_user_armor"),
    ]

    operations = [
        migrations.RunPython(create_initial_superuser, drop_initial_superuser)
    ]
