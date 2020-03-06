from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField


class Subject(models.Model):
    title = models.CharField('Назва предмету', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предмети'

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE, verbose_name='Автор')
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE, verbose_name='Предмет')
    title = models.CharField('Назва курсу', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField('Короткий опис')
    created = models.DateTimeField('Дата створення', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курси'

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField('Назва модулю', max_length=200)
    description = models.TextField('Опис', blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

    class Meta:
        ordering = ['order']
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модулі'


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Контент'
        verbose_name = 'Контент'


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField('Назва матеріалу', max_length=250)
    created = models.DateTimeField('Створено', auto_now_add=True)
    updated = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексти'


class File(ItemBase):
    file = models.FileField(upload_to='files')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файли'


class Image(ItemBase):
    file = models.FileField(upload_to='images')

    class Meta:
        verbose_name = 'Зображення'
        verbose_name_plural = 'Зображення'


class Video(ItemBase):
    url = models.URLField()

    class Meta:
        verbose_name = 'Відео'
        verbose_name_plural = 'Відео'
