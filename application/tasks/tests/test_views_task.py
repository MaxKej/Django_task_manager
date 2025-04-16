import pytest
from django.urls import reverse
from tasks.models import Task
from django.contrib.auth.models import User
from simple_history.utils import update_change_reason


@pytest.mark.django_db
def test_task_detail_view(client):
    user = User.objects.create_user(username='user1', password='test1234')
    task = Task.objects.create(nazwa='Test', status='Nowy', autor=user)
    url = reverse('task_detail', args=[task.id])
    response = client.get(url)
    assert response.status_code == 200
    assert task.nazwa.encode() in response.content

@pytest.mark.django_db
def test_create_task_view(client):
    user = User.objects.create_user(username='apiuser', password='secret')
    client.login(username='apiuser', password='secret')

    url = reverse('add_task')
    response = client.post(url, {
        'nazwa': 'Zadanie API',
        'status': 'Nowy'
    })

    assert response.status_code == 302
    assert Task.objects.filter(nazwa='Zadanie API', status='Nowy', autor=user).exists()

@pytest.mark.django_db
def test_delete_task_view(client):
    user = User.objects.create_user(username='deleter', password='pass')
    task = Task.objects.create(nazwa='Do usunięcia', status='Nowy', autor=user)

    client.login(username='deleter', password='pass')
    url = reverse('delete_task', args=[task.id])
    response = client.post(url)
    assert response.status_code == 302
    assert not Task.objects.filter(id=task.id).exists()

@pytest.mark.django_db
def test_filter_tasks_by_name(client):
    user = User.objects.create_user(username='filtrujący', password='pass')
    Task.objects.create(nazwa='Unikalna nazwa', status='Nowy', autor=user)
    Task.objects.create(nazwa='Inna', status='W toku', autor=user)

    url = reverse('filter_tasks') + '?nazwa=Unikalna'
    response = client.get(url)
    assert response.status_code == 200
    assert b'Unikalna nazwa' in response.content
    assert b'Inna' not in response.content


