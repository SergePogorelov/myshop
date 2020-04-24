from __future__ import absolute_import, unicode_literals

import os

from celery import Celery


# Задаем переменную окружения, содержащую название файла настроек нашего проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celary('myshop')

app.config_from_object('django.conf:settings', namespase='CELERY')
app.autodiscover_tasks()

# В этом коде мы выполняем следующие действия:
# 1)	задаем переменную окружения DJANGO_SETTINGS_MODULE для консольных
# команд Celery;
# 2) создаем экземпляр приложения с помощью записи app = Celery('myshop');
# 3)	загружаем конфигурацию из настроек нашего проекта, вызывая метод
# config_from_object(). Параметр namespace определяет префикс, который
# мы будем добавлять для всех настроек, связанных с Celery. Таким об-
# разом, в файле settings.py можно будет задавать конфигурацию Celery
# через настройки вида CELERY_, например CELERY_BROKER_URL;
# 4)	наконец, вызываем процесс поиска и загрузки асинхронных задач по
# нашему проекту. Celery пройдет по всем приложениям, указанным в на-
# стройке INSTALLED_APPS, и попытается найти файл tasks.py, чтобы загру-
# зить код задач.

# Вам необходимо импортировать модуль celery.py в файле __init__.py про-
# екта, чтобы он выполнялся при старте проект

