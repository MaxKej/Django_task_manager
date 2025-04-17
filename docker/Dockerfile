FROM python:latest

# Dodaj użytkownika
RUN useradd -m -s /bin/bash hosting && \
    echo 'hosting ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER hosting
WORKDIR /home/hosting

# Utwórz i aktywuj środowisko wirtualne
RUN python -m venv venv
ENV PATH="/home/hosting/venv/bin:$PATH"

# Zainstaluj wymagane pakiety Python/Django
RUN pip install --upgrade pip && \
    pip install \
        Django==5.2 \
        djangorestframework \
        psycopg2-binary \
        django-filter \
        gunicorn \
        whitenoise \
        python-decouple \
        dj-database-url \
        django-simple-history \
        pytest \
        pytest-django

# Ustaw katalog projektu jako working directory
WORKDIR /home/hosting/app

CMD ["bash"]
