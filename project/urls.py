from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('todo/', include(('todo.urls', 'todo'), namespace='todo')),
    path('users/', include('users.urls')),
]