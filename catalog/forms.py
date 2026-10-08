
from pathlib import Path

from PIL import Image
from django import forms
from django.core.exceptions import ValidationError

from .models import Product


FORBIDDEN_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "form-select"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {"class": "form-control", "rows": 4}
                )
            else:
                field.widget.attrs.update({"class": "form-control"})

    def _validate_forbidden_words(self, value):
        normalized_value = value.casefold()

        for word in FORBIDDEN_WORDS:
            if word.casefold() in normalized_value:
                raise ValidationError(
                    f"Текст содержит запрещённое слово: «{word}»."
                )

        return value

    def clean_name(self):
        name = self.cleaned_data["name"]
        return self._validate_forbidden_words(name)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return self._validate_forbidden_words(description)

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")

        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            return image

        max_size = 5 * 1024 * 1024

        if image.size > max_size:
            raise ValidationError("Размер изображения не должен превышать 5 МБ.")

        try:
            with Image.open(image) as img:
                if img.format not in ("JPEG", "PNG"):
                    raise ValidationError(
                        "Допустимые форматы изображения: JPEG и PNG."
                    )
                img.verify()
        except ValidationError:
            raise
        except Exception as exc:
            raise ValidationError(
                "Не удалось прочитать изображение. Загрузите корректный JPEG или PNG."
            ) from exc

        image.seek(0)
        return image