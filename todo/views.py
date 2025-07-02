from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo
from .models import Todo, Notification # Import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

# Assuming your ListView for todos looks something like this
class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/list.html' # Or your template name
    context_object_name = 'todos'

    def get_queryset(self):
        # Ensure users only see their own todos
        return Todo.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the unread notifications
        context['notifications'] = Notification.objects.filter(user=self.request.user, is_read=False).order_by('-created_at')
        return context

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