from django.db import migrations

def create_roles_and_permissions(apps, schema_editor):
    Role = apps.get_model("users", "Role")
    Module = apps.get_model("users", "Module")
    RolePermissions = apps.get_model("users", "RolePermissions")

    catalog, _ = Module.objects.get_or_create(name="Catalog", defaults={"description": "Каталог товаров"})
    cart, _ = Module.objects.get_or_create(name="Cart", defaults={"description": "Корзина магазина"})

    guest, _ = Role.objects.get_or_create(name="guest", defaults={"description": "Гость"})
    user, _ = Role.objects.get_or_create(name="user", defaults={"description": "Пользователь"})
    moderator, _ = Role.objects.get_or_create(name="moderator", defaults={"description": "Модератор"})
    admin, _ = Role.objects.get_or_create(name="admin", defaults={"description": "Администратор"})

    RolePermissions.objects.get_or_create(role=guest, module=catalog, defaults={"read_permission": True})

    RolePermissions.objects.get_or_create(role=user, module=catalog, defaults={"read_permission": True})
    RolePermissions.objects.get_or_create(role=user, module=cart, defaults={
        "read_permission": True,
        "create_permission": True,
        "update_permission": True,
        "delete_permission": True,
    })

    RolePermissions.objects.get_or_create(role=moderator, module=catalog, defaults={
        "read_permission": True,
        "update_permission": True,
    })
    RolePermissions.objects.get_or_create(role=moderator, module=cart, defaults={
        "read_permission": True,
        "create_permission": True,
        "update_permission": True,
        "delete_permission": True,
    })

    RolePermissions.objects.get_or_create(role=admin, module=catalog, defaults={
        "read_permission": True,
        "create_permission": True,
        "update_permission": True,
        "delete_permission": True,
    })
    RolePermissions.objects.get_or_create(role=admin, module=cart, defaults={
        "read_permission": True,
        "create_permission": True,
        "update_permission": True,
        "delete_permission": True,
    })


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_roles_and_permissions),
    ]
