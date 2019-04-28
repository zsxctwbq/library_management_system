from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户表
class User(AbstractUser):
    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户'


# 出版社
class Publisher(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称', unique=True)
    addr = models.CharField(max_length=128, null=True, verbose_name='地址')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '出版社'


# 书
class Book(models.Model):
    title = models.CharField(max_length=64, null=False, unique=True, verbose_name='书名')
    publisher = models.ForeignKey(to='Publisher', null=True, verbose_name='出版社')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '图书'


class Author(models.Model):
    name = models.CharField(max_length=16, null=False, unique=True, verbose_name='姓名')
    book = models.ManyToManyField(to="Book")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '作者'
