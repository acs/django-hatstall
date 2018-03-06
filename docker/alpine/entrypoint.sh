#!/bin/sh

echo "Running Hatstall"

/usr/local/bin/python3 manage.py collectstatic -l --noinput
/usr/local/bin/python3 manage.py makemigrations
/usr/local/bin/python3 manage.py migrate

# Create an admin user
/usr/local/bin/python3 manage.py shell -c "
from django.contrib.auth.models import User
import os
user = os.getenv('HATSTALL_ADMIN_USER','admin')
mail = os.getenv('HATSTALL_ADMIN_MAIL','admin@example.com')
password = os.getenv('HATSTALL_ADMIN_PASS','admin')

User.objects.create_superuser(user , mail, password ) 
print(\"Add admin user:\n\tuser: {}\n\temail {}\".format(user,mail))
"

echo "Hatstall service running on http://localhost:8000"
# python3 manage.py runserver 0.0.0.0:8000
gunicorn django_hatstall.wsgi --workers "$HATSTALL_GUNICORN_WORKERS" --timeout "$HATSTALL_GUNICORN_TIMEOUT" --bind 0.0.0.0:8000
