import time
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import AttemptedMailing


def send_mailing(mailing):
    recipients = list(mailing.recipients.values_list('email', flat=True))

    mailing.status = 'running'
    mailing.start_time = timezone.now()
    mailing.save()

    for email in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            AttemptedMailing.objects.create(
                mailing=mailing,
                status='succeed',
                mail_server_response=f"Письмо успешно отправлено на {email} ({timezone.now()})",
            )
        except Exception as e:
            AttemptedMailing.objects.create(
                mailing=mailing,
                status='failed',
                mail_server_response=f"Ошибка при отправке на {email}: {str(e)}",
            )

    mailing.status = 'finished'
    mailing.end_time = timezone.now()
    mailing.save()