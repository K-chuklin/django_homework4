import itertools

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.text import slugify


NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    name = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.SlugField(max_length=150, db_index=True, verbose_name='URL', **NULLABLE)
    content = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='images/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    published = models.BooleanField(verbose_name='признак публикации', default=True)
    view_count = models.PositiveIntegerField(verbose_name='количество просмотров', default=0)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        return super().save(*args, **kwargs)

    def _generate_slug(self):
        slug_candidate = slugify(self.name)
        if not slug_candidate:
            slug_candidate = "s"
        for i in itertools.count(1):
            if not Post.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_candidate, i)
        self.slug = slug_candidate
        return self.slug

    def get_absolute_url(self):
        return reverse('blog:post_item', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('created_at',)

    def increase_view_count(self):
        self.view_count += 1
        self.save()
