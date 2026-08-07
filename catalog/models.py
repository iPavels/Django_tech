from django.db import models

class Product(models.Model):
    name=models.CharField(max_length=100, verbose_name='наименование', help_text='Введите наименование')
    description=models.TextField(max_length=500, verbose_name='описание')
    image=models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='изображение')
    category=models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at=models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Продукт'
        verbose_name_plural='Продукты'




class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование', help_text='Введите наименование')
    description = models.TextField(max_length=500, verbose_name='описание')