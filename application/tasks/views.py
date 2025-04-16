from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseBadRequest, HttpResponseForbidden



def home_view(request):
    return render(request, 'tasks/home.html')



@login_required
def dashboard_view(request):
    moje_zadania = Task.objects.filter(autor=request.user)
    przypisane_do_mnie = Task.objects.filter(przypisany_uzytkownik=request.user)

    return render(request, 'tasks/dashboard.html', {
        'moje_zadania': moje_zadania,
        'przypisane_do_mnie': przypisane_do_mnie,
    })


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rejestracja zakończona sukcesem! Możesz się teraz zalogować.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'status', 'przypisany_uzytkownik']
    search_fields = ['nazwa', 'opis']
    permission_classes = [IsAuthenticatedOrReadOnly]


def perform_create(self, serializer):
    serializer.save(autor=self.request.user)

@login_required
def add_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.autor = request.user
            task.save()
            messages.success(request, 'Pomyślnie dodano zadanie!')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})


def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)  # odświeżenie widoku szczegółów
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


def can_user_delete_task(user, task):
    return user.is_staff or task.autor == user

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if not can_user_delete_task(request.user, task):
        return HttpResponseForbidden("Nie masz uprawnień do usunięcia tego zadania!")

    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')

    return render(request, 'tasks/confirm_delete.html', {'task': task})

def task_at_time_view(request, task_id):
    timestamp = request.GET.get("timestamp")
    task = get_object_or_404(Task, id=task_id)

    if not timestamp:
        return HttpResponseBadRequest("Brak parametru ?timestamp=YYYY-MM-DDTHH:MM")

    try:
        dt = parse_datetime(timestamp)
        if dt is None:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Nieprawidłowy format daty. Użyj ?timestamp=YYYY-MM-DDTHH:MM")

    # znajdź wersję historii sprzed tej daty
    history = task.history.filter(history_date__lte=dt).order_by('-history_date').first()

    return render(request, 'tasks/task_at_time.html', {
        'history': history,
        'timestamp': dt,
        'task': task,
    })


def task_history_view(request, task_id=None):
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        history = task.history.all()
    else:
        history = Task.history.all()

    return render(request, 'tasks/task_history.html', {
        'history': history,
        'task_id': task_id,
        'task': task,
    })

def filter_task_history_view(request):
    task_id = request.GET.get('id')
    nazwa = request.GET.get('nazwa')
    status = request.GET.get('status')
    przypisany = request.GET.get('user')
    edytowal = request.GET.get('changed_by')

    history = Task.history.all()

    if task_id:
        history = history.filter(id=task_id)

    if nazwa:
        history = history.filter(nazwa__icontains=nazwa)

    if status:
        history = history.filter(status=status)

    if przypisany:
        history = history.filter(przypisany_uzytkownik__username__icontains=przypisany)

    if edytowal:
        history = history.filter(history_user__username__icontains=edytowal)

    return render(request, 'tasks/filter_task_history.html', {'history': history})

def filter_tasks_view(request):
    query = request.GET.get('q')
    status = request.GET.get('status')
    user_name = request.GET.get('user')
    task_id = request.GET.get('id')
    nazwa = request.GET.get('nazwa')
    opis = request.GET.get('opis')
    sort_by = request.GET.get('sort_by')

    tasks = Task.objects.all()

    if task_id:
        tasks = tasks.filter(id=task_id)
    if nazwa:
        tasks = tasks.filter(nazwa__icontains=nazwa)
    if opis:
        tasks = tasks.filter(opis__icontains=opis)
    if status:
        tasks = tasks.filter(status=status)
    if user_name:
        tasks = tasks.filter(przypisany_uzytkownik__username__icontains=user_name)

    # sortowanie
    if sort_by == 'created_at_desc':
        tasks = tasks.order_by('-created_at')
    elif sort_by == 'created_at_asc':
        tasks = tasks.order_by('created_at')
    elif sort_by == 'updated_at_desc':
        tasks = tasks.order_by('-updated_at')
    elif sort_by == 'updated_at_asc':
        tasks = tasks.order_by('updated_at')

    return render(request, 'tasks/filter_tasks.html', {'tasks': tasks})