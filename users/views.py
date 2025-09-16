from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER
from .forms import UserRegisterForm
from django.core.mail import send_mail


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Subject test'
        message = 'Message test'
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)
