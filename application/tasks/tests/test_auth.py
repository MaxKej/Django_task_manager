import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_register_view(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'password1': 'pass123456!',
        'password2': 'pass123456!',
    })
    assert response.status_code == 302
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_login_view(client, django_user_model):
    django_user_model.objects.create_user(username='test', password='pass1234')
    response = client.post(reverse('api_login'), {'username': 'test', 'password': 'pass1234'})
    assert response.status_code == 200
