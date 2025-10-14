from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View

from config.settings import EMAIL_HOST_USER
from .forms import UserRegisterForm
from django.core.mail import send_mail

from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.http import HttpResponse


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('messanger:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        confirm_link = self.request.build_absolute_uri(
            reverse('users:confirm_email', args=[user.id])
        )

        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для активации аккаунта перейдите по ссылке:\n{confirm_link}\n\n',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        self.send_welcome_email(user.email)
        return HttpResponse("Ссылка на подтверждение отправлена")

    def send_welcome_email(self, user_email):
        subject = 'Welcome letter test'
        message = 'Welcome letter message test'
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class ConfirmEmailView(View):
    template_name= 'users/confirm_email.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = True
        user.save()
        return render('users:confirm_email')
