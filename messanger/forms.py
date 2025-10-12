from django import forms
from .models import Message, Mailing, Recipient
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'message']

    def __init__(self, *args, **kwargs):

        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Тема'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Сообщение'})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['recipients', 'message']

    def __init__(self, *args, **kwargs):

        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['recipients'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Получтель'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Сообщение'})



class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'fullname', 'comment']

    def __init__(self, *args, **kwargs):

        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email получтеля'})
        self.fields['fullname'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ф.И.о получтеля'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Коментарий'})
