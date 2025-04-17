# Django task manager

---

# Uruchomienie aplikacji

## Zbudowanie aplikacji w docker
docker-compose up --build

## Wejdź do kontenera web
docker-compose exec web bash

## Wykonaj migracje
python manage.py migrate

## Utwórz superużytkownika
python manage.py createsuperuser

## Wykonanie testów
docker-compose exec web pytest tasks/tests/

## Uruchomienie aplikacji poprzez gunicorn
cd /home/hosting/app
gunicorn --pythonpath . application.wsgi:application --bind 0.0.0.0:8000

---

# Korzystanie z endpointów aplikacji za pomocą `curl`

Aplikacja obsługuje logowanie i zarządzanie zadaniami z użyciem komendy `curl`, przy wykorzystaniu ciasteczek sesyjnych i tokena CSRF.


### Logowanie (z użyciem `/accounts/login/`)

#### Pobierz ciasteczka i token CSRF:

curl -c cookies.txt http://localhost:8000/accounts/login/

token csrf znajduje się w elemencie input z parametrami type="hidden" name="csrfmiddlewaretoken" value="CSRF_TOKEN"

#### Zalogowanie użytkownika

curl -X POST http://localhost:8000/accounts/login/ \
  -b cookies.txt \
  -c cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "csrfmiddlewaretoken=CSRF_TOKEN&username=UserCurl&password=NoweHaslo123"

#### Rejestracja użytkownika:

curl -X POST http://localhost:8000/register/ \
  -b cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "csrfmiddlewaretoken=CSRF_TOKEN&username=UserCurl&password1=NoweHaslo123&password2=NoweHaslo123"

#### Dodanie zadania:

curl -X POST http://localhost:8000/zadania/dodaj/ \
  -b cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "csrfmiddlewaretoken=CSRF_TOKEN&nazwa=Zadanie testowe&opis=To jest test&status=Nowy"

#### Filtrowanie zadań:

curl -G http://localhost:8000/zadania/filtruj/ \
  -b cookies.txt \
  --data-urlencode "nazwa=test" \
  --data-urlencode "status=Nowy"

#### Usunięcie zadania:

curl -X POST http://localhost:8000/zadania/10/usun/ \
  -b cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "csrfmiddlewaretoken=CSRF_TOKEN"

#### Wylogowanie:

curl -X POST http://localhost:8000/accounts/logout/ \
  -b cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "csrfmiddlewaretoken=CSRF_TOKEN"

