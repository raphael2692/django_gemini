from django.urls import path
from . import views

urlpatterns = [
    path("", views.TodoList.as_view(), name="list"),
    path("create/", views.TodoCreate.as_view(), name="todo_create"),
    path("<int:pk>/edit/", views.TodoUpdate.as_view(), name="todo_edit"),
    path("<int:pk>/delete/", views.TodoDelete.as_view(), name="todo_delete"),
]
