FROM ubuntu:24.04

# Zainstaluj wymagane pakiety systemowe
RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install build-essential curl sudo python3 python3-pip python3-venv libpq-dev

# Dodaj użytkownika
RUN useradd -m -s /bin/bash hosting && \
    echo 'hosting ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER hosting
WORKDIR /home/hosting

# Utwórz i aktywuj środowisko wirtualne
RUN python3 -m venv venv
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

# Ustaw domyślny working dir
WORKDIR /home/hosting/app

CMD ["bash"]
