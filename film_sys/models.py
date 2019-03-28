from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    username = models.CharField(max_length=64, verbose_name='username', unique=True)
    email = models.EmailField(max_length=64, verbose_name='email', default='')
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )


class IndexLabel(models.Model):
    name = models.CharField(max_length=64, verbose_name='name')

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=64, verbose_name='name')
    index_label = models.ForeignKey('IndexLabel', verbose_name='index_label', related_name='label', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Film(models.Model):
    label = models.ForeignKey('Label', verbose_name='label', related_name='film',  on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64, verbose_name='name')
    cover = models.ImageField(upload_to='images', blank=True)
    film_file = models.FileField(upload_to='film', default='', blank=True)
    score = models.CharField(max_length=64, verbose_name='score', blank=True)
    released = models.CharField(max_length=64, verbose_name='released', blank=True)
    introduction = models.TextField(verbose_name='introduction', default='', blank=True)
