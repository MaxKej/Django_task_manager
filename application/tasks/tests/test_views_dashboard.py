import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_dashboard_view_authenticated(client):
    user = User.objects.create_user(username='user1', password='pass')
    client.login(username='user1', password='pass')
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_view_unauthenticated(client):
    response = client.get(reverse('dashboard'))
    assert response.status_code == 302
