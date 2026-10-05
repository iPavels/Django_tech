from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Создаёт группу модераторов продуктов и выдаёт необходимые права"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Модератор продуктов"
        )

        permissions = Permission.objects.filter(
            content_type__app_label="catalog",
            codename__in=[
                "delete_product",
                "can_unpublish_product",
            ],
        )

        group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f'Группа "{group.name}" настроена. '
                f"Выдано прав: {permissions.count()}"
            )
        )