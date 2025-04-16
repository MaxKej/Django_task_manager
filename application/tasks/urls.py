from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, add_task_view, filter_tasks_view, task_detail_view, edit_task_view, delete_task_view
from .views import task_at_time_view, task_history_view, filter_task_history_view
from .views import home_view, register_view, dashboard_view
from .views_auth import LoginApiView
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'zadania', TaskViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('api/login/', LoginApiView.as_view(), name='api_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('zadania/dodaj/', add_task_view, name='add_task'),
    path('zadania/filtruj/', filter_tasks_view, name='filter_tasks'),
    path('zadania/<int:task_id>/', task_detail_view, name='task_detail'),
    path('zadania/<int:task_id>/edytuj/', edit_task_view, name='edit_task'),
    path('zadania/<int:task_id>/usun/', delete_task_view, name='delete_task'),
    path('zadania/<int:task_id>/stan/', task_at_time_view, name='task_at_time'),
    path('zadania/historia/', task_history_view, name='task_history_all'),
    path('zadania/<int:task_id>/historia/', task_history_view, name='task_history'),
    path('zadania/historia/filtruj/', filter_task_history_view, name='task_history_filter'),
    path('', include(router.urls)),
]
