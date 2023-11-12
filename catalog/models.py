from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория продукта")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    created_at = models.DateTimeField(**NULLABLE, verbose_name='Время создания')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, verbose_name="Категория продукта")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    image = models.ImageField(upload_to='catalog/', **NULLABLE)
    price = models.IntegerField(default=0, verbose_name='Стоимость')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='продавец')
    creation_date = models.DateField(**NULLABLE, verbose_name='Дата создания')
    last_modification_date = models.DateField(**NULLABLE, verbose_name='Дата последнего изминения')

    views_counter = models.IntegerField(default=0, verbose_name='просмотры')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)

    def __str__(self):
        return f'{self.name}{self.price}'

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'


class Version(models.Model):
    VERSION_CHOICES = ((True, 'активная'), (False, 'не активная'))

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    version_number = models.CharField(max_length=50, verbose_name='версия продукта')
    name_version = models.CharField(max_length=100, verbose_name='название версии')
    current_version_indicator = models.BooleanField(choices=VERSION_CHOICES, verbose_name='индикатор текущей версии')

    def __str__(self):
        return f'{self.name_version} ({self.version_number})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        ordering = ('version_number',)


@receiver(post_save, sender=Version)
def set_current_version(sender, instance, **kwargs):
    if instance.current_version_indicator:
        Version.objects.filter(product=instance.product).exclude(pk=instance.pk).update(current_version_indicator=False)
