from django.urls import path
from . import views

app_name = 'messanger'

urlpatterns = [
    path('new_mailing/', views.MailingCreate.as_view(), name='mailing_create'),
    path('change_mailing/<int:pk>/', views.MailingUpdate.as_view(), name='mailing_update'),
    path('delete_mailing/<int:pk>/', views.MailingDelete.as_view(), name='mailing_delete'),
    path('new_message/', views.MessageCreate.as_view(), name='message_create'),
    path('update_message/<int:pk>/', views.MessageUpdate.as_view(), name='message_update'),
    path('delete_message/<int:pk>/', views.MessageDelete.as_view(), name='message_delete'),
    path('new_recipient/', views.RecipientCreate.as_view(), name='recipient_create'),
    path('change_recipient/<int:pk>/', views.RecipientUpdate.as_view(), name='recipient_update'),
    path('delete_recipient/<int:pk>/', views.RecipientDelete.as_view(), name='recipient_delete'),
    path('home/', views.HomeView.as_view(), name='home'),
]
