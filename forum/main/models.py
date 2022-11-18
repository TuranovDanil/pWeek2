from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + ' ' + filename])


def validate_image_size(img):
    filesize = img.file.size
    megabyte_max = 2.0
    if filesize > megabyte_max * 1024 * 1024:
        raise ValidationError("Максимальный размер %sMB" % str(megabyte_max))


class AbsUser(AbstractUser):
    name = models.CharField(max_length=60, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=60, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=60, verbose_name='Отчество', blank=False)
    username = models.CharField(max_length=60, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=60, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=60, verbose_name='Пароль', unique=True, blank=False)
    role = models.CharField(max_length=60, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')
    personal_data = models.BooleanField(default=False, verbose_name='Согласие на обработку данных', blank=False)

    # USERNAME_FIELD = username

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname) + ' (' + str(self.username) + ')'

    # class Meta(AbstractUser.Meta):
    #     pass


class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'новая'),
        ('work', 'принято в работу'),
        ('completed', 'выполнено')
    ]
    name = models.CharField(max_length=250, verbose_name='Имя', blank=False)
    description = models.CharField(max_length=250, verbose_name='Описание', blank=False)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    photo = models.ImageField(upload_to=get_name_file,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                          validate_image_size],
                              blank=False)
    status = models.CharField(max_length=60, verbose_name='Статус',
                              choices=(('new', 'новая'), ('work', 'принято в работу'), ('completed', 'выполнено')),
                              default='new', blank=False)
    user = models.ForeignKey('AbsUser', verbose_name='Заказчик', on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=250, verbose_name='Комментрарий', blank=True, null=True)
    photo2 = models.ImageField(upload_to=get_name_file,
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                           validate_image_size],
                               blank=True, null=True)

    def __str__(self):
        return str(self.name) + ' ' + str(self.category)


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя', blank=False)

    def __str__(self):
        return str(self.name)
