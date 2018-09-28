Project installation steps:
1) Create new database with 'UTF-8' character set.
On mysql it will be:
'CREATE DATABASE rent CHARACTER SET utf8 COLLATE utf8_general_ci'

2) In settings.py at DATABASES dictionary change your database settings.

3) Open the terminal in /rent_site directory and type:
python3 manage.py makemigrations
python3 manage.py migrate

4) At the same directory in terminal create super user by:
python3 manage.py createsuperuser

5) At the same directory in terminal start server by:
python3 manage.py runserver

Development server address will be printed in terminal.


