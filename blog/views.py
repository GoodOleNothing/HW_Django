from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from .models import Blog

# Create your views here.


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(active=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        count = super().get_object()
        count.views_count += 1
        count.save(update_fields=['views_count'])
        if count.views_count == 10:
            send_mail(
                subject="100 просмотров",
                message=f"Запись '{count.title}' достигла 100 просмотров",
                recipient_list=["email@example.com"],
            )
        return count


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'image', 'active']
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'image', 'active']

    def get_success_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
