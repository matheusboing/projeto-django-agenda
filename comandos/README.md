```
Configuração Git:

git config --global user.name 'matheusboing'
git config --global user.email 'matboing@hotmail.com'
git config --global init.defaultBranch main
git init

git add .
git commit -m 'Mensagem'
git remote add origin git@github.com:matheusboing/projeto-agenda-django.git
```

```
python -m venv venv
. venv/bin/activate
pip install django
django-admin startproject project .
python manage.py startapp contact
```