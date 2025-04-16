from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Task(models.Model):
    STATUS_CHOICES = [
        ('Nowy', 'Nowy'),
        ('W toku', 'W toku'),
        ('Rozwiązany', 'Rozwiązany'),
    ]

    nazwa = models.CharField(max_length=255)
    opis = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Nowy')
    przypisany_uzytkownik = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='zadania'
    )
    autor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='zadania_utworzone'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.nazwa
