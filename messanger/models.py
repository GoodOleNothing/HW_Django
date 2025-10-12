from django.db import models
from django.conf import settings


class Message(models.Model):
    subject = models.CharField(max_length=50, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Сообщение')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messagetowner',
                              null=True, blank=True)

    def __str__(self):
        return f'{self.subject}, {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Recipient(models.Model):
    email = models.CharField(max_length=40, verbose_name='email', unique=True)
    fullname = models.CharField(max_length=130, verbose_name='Ф.И.О')
    comment = models.CharField(max_length=300, verbose_name='Коментарий')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipientowner',
                              null=True, blank=True)

    def __str__(self):
        return f'{self.email}, {self.fullname}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('finished', 'Завершена'),
    ]
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время первой отправки')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания отправки')
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение')
    recipients = models.ManyToManyField(Recipient, related_name='recipients', verbose_name='Получатели')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner',
                              null=True, blank=True)


    def __str__(self):
        return f"Рассылка {self.id} — {self.status}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class AttemptedMailing(models.Model):
    STATUS_CHOICES = [
        ('succeed', 'Успешно'),
        ('failed', 'Не успешно'),
    ]
    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True, verbose_name='Статус')
    mail_server_response = models.TextField(verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing', verbose_name='Рассылка')

    def __str__(self):
        return f"Попытка {self.id} — {self.status}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'



