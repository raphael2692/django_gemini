from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todo/list.html"

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoCreate(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title", "description", "completed"]
    template_name = "todo/form.html"
    success_url = reverse_lazy("todo:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ["title", "description", "completed"]
    template_name = "todo/form.html"
    success_url = reverse_lazy("todo:list")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = "todo/confirm_delete.html"
    success_url = reverse_lazy("todo:list")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)