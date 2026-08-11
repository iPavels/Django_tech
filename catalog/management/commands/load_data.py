from django.core.management import BaseCommand, call_command

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Удаляет существующие данные и загружает тестовые данные"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "catalog/fixtures/categories.json")
        call_command("loaddata", "catalog/fixtures/products.json")

        self.stdout.write(
            self.style.SUCCESS("Тестовые данные успешно загружены")
        )