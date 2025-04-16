import pytest
from django.urls import reverse
from tasks.models import Task
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_task_history_view(client):
    user = User.objects.create_user(username='user', password='pass')
    task = Task.objects.create(nazwa='Historia Test', status='Nowy', autor=user)
    url = reverse('task_history', args=[task.id])
    client.login(username='user', password='pass')
    response = client.get(url)
    assert response.status_code == 200
