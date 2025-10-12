from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Message, Recipient, Mailing, AttemptedMailing
from users.models import User
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .forms import MessageForm, MailingForm, RecipientForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .utils import send_mailing
# Create your views here.


class MailingCreate(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('messanger:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        selected_recipients = form.cleaned_data.get('recipients', [])
        for owners in selected_recipients:
            if owners.owner != self.request.user:
                return HttpResponseForbidden("Вы не владелец. У вас нет прав на добавление этого получателя")
        return super().form_valid(form)


class MailingUpdate(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'messanger/mailing_update.html'
    success_url = reverse_lazy('messanger:home')

    def dispatch(self, request, *args, **kwargs):
        mailing = self.get_object()
        if mailing.owner != request.user:
            return HttpResponseForbidden("Вы не владелец. У вас нет прав на редактирование этой рассылки")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        selected_recipients = form.cleaned_data.get('recipients', [])
        for owners in selected_recipients:
            if owners.owner != self.request.user:
                return HttpResponseForbidden("Вы не владелец. У вас нет прав на добавление этого получателя")
        return super().form_valid(form)


class MailingDelete(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('messanger:home')

    def dispatch(self, request, *args, **kwargs):
        mailing = self.get_object()
        if mailing.owner != request.user:
            return HttpResponseForbidden("Вы не владелец. У вас нет прав на удаление этой рассылки")
        return super().dispatch(request, *args, **kwargs)


class MessageCreate(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messanger:home')


class MessageUpdate(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messanger/message_update.html'
    success_url = reverse_lazy('messanger:home')

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.owner != request.user:
            return HttpResponseForbidden("Вы не владелец. У вас нет прав на изменение этого сообщения")
        return super().dispatch(request, *args, **kwargs)


class MessageDelete(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('messanger:home')

    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.owner != request.user:
            return HttpResponseForbidden("Вы не владелец. У вас нет прав на уадление этого сообщения")
        return super().dispatch(request, *args, **kwargs)


class RecipientCreate(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('messanger:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdate(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'messanger/recipient_update.html'
    success_url = reverse_lazy('messanger:home')

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        if recipient.owner != request.user:
            return HttpResponseForbidden("Вы не владелец. У вас нет прав на редактирование этого получателя")
        return super().dispatch(request, *args, **kwargs)


class RecipientDelete(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy('messanger:home')

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        if recipient.owner != request.user:
            return HttpResponseForbidden("Вы не владелец. У вас нет прав на уадление этого получателя")
        return super().dispatch(request, *args, **kwargs)


class HomeView(ListView):
    model = Mailing
    template_name = 'messanger/home.html'

    def get_queryset(self):
        data = cache.get('mailings_list')
        if not data:
            data = Mailing.objects.all()
            cache.set('mailings_list', data, 60 * 15)
        return data

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if 'user_id' in request.POST:
                if not request.user.groups.filter(name="Mailing Manager").exists():
                    return HttpResponseForbidden("У вас нет прав на блокировку пользователей")

                user_id = request.POST.get('user_id')
                user = get_object_or_404(User, id=user_id)
                if not user.is_superuser:
                    user.is_active = not user.is_active
                    user.save()

                return redirect('messanger:home')

            elif 'mailing_id' in request.POST:
                mailing = get_object_or_404(Mailing, id=request.POST.get('mailing_id'))
                if mailing.owner != request.user:
                    return HttpResponseForbidden("Вы не владелец этой рассылки")

            send_mailing(mailing)
            return redirect('messanger:home')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_of_mailings'] = Mailing.objects.count()
        context['number_of_mailings_running'] = Mailing.objects.filter(status='running').count()
        context['unique_recipients'] = Recipient.objects.count()
        context['is_manager'] = self.request.user.groups.filter(name="Mailing Manager").exists()
        context['users_list'] = [i for i in User.objects.all()]
        context['recipients_list'] = [i.email for i in Recipient.objects.all()]
        if self.request.user.is_authenticated:
            mailing = Mailing.objects.get(owner=self.request.user)
            context['successfull_attempts'] = AttemptedMailing.objects.filter(status='succeed', mailing=mailing).count()
            context['unsuccessfull_attempts'] = AttemptedMailing.objects.filter(status='failed', mailing=mailing).count()
            context['message_count'] = AttemptedMailing.objects.filter(mailing=mailing).count()
        return context




