from django.db import models
from django.conf import settings


class Message(models.Model):
    subject = models.CharField(max_length=50, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.subject}, {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MessageReceiver(models.Model):
    email = models.CharField(max_length=40, verbose_name='email', unique=True)
    fullname = models.CharField(max_length=130, verbose_name='Ф.И.О')
    comment = models.CharField(max_length=300, verbose_name='Коментарий')

    def __str__(self):
        return f'{self.email}, {self.fullname}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

