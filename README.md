# Интернет магазин

Интернет-магазин c  каталогом товаров, корзиной и возможностью оформления заказов. 

### Основной функционал:
- каталог товаров пополняемый через админку;
- корзина реализована с помощью `сессий Django`;
- в админке магазина динамически формируются счета в `PDF`;
- упарвление и выгрузка заказов в `CSV`;
- после создания заказа  на электронную почту пользователей отправляется `pdf-счет` в асинхронном режиме через `Celery`;
- реализована система скидок (купонов) и рекомендация товаров с помощью `Redis`;
- настроена локализация на 2 языка: `русский` и `английсикй`.

## Установка
Эти инструкции помогут вам создать копию проекта и запустить ее на локальном компьютере для целей разработки и тестирования.

**Перед тем, как начать:**
1. Если вы не пользуетесь `Python 3`, вам нужно будет установить инструмент `virtualenv` при помощи `pip install virtualenv`. 
Если вы используете `Python 3`, у вас уже должен быть модуль [venv](https://docs.python.org/3/library/venv.html), установленный в стандартной библиотеке.

2. Установите `Redis`. Воспользуйтесь [инструкциями с официального сайта](https://redis.io/download) или командами:
```
wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable && make
```
Запустите сервер `Redis` командой `src/redis-server` из папки `redis-stable`

3. Для работы c `Celery` необходим посредник (брокер). 
Устнаовите `RabbitMQ` - он является рекомендуемым брокером для `Celery`
```
echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install rabbitmq-server
```
Запустите сервер `RabbitMQ`
```
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
```
[Подробнее об уствновке](https://www.rabbitmq.com/download.html) на официальном сайте `RabbitMQ`

### Запуск проекта (на примере Linux)
- Создайте на своем компютере папку проекта `mkdir myshop` и перейдите в нее `cd myshop`
- Склонируйте этот репозиторий в текущую папку `git clone https://github.com/SergePogorelov/myshop.git .`
- Создайте виртуальное окружение `python3 -m venv venv`
- Активируйте виртуальное окружение `source venv/bin/activate`
- Установите зависимости `pip install -r requirements.txt`
- Накатите миграции `python manage.py migrate`
- Создайте суперпользователя Django `python manage.py createsuperuser --username admin --email 'admin@example.com'`
- Запустите сервер разработки Django `python manage.py runserver`
- Откройте другую консоль и запустите процесс `Celery` из папки проекта с помощью команды `celery -A myshop worker -l info`
- Для локального тестирования вы можете загрузить данные из фикстур `python manage.py loaddata fixtures.json`

**Мониторинг Celery**

Для отслеживаия выполнения задач будем использовать [Flower](https://flower.readthedocs.io/en/latest/). 
Запустите `Flower` из папки проекта командой `celery -A myshop flower` и откройте в браузере `http://localhost:5555/dashboard`

## В разработке использованы

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Sorl-thumbnail](https://pypi.org/project/sorl-thumbnail/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryproject.org/en/stable/)
- [Flower](https://flower.readthedocs.io/en/latest/)
- [RabbitMQ](https://www.rabbitmq.com/)

## Лицензия
Этот проект лицензируется по лицензии `BSD 3-Clause License` - см. [LICENSE.md](https://github.com/SergePogorelov/myshop/blob/master/LICENSE) для получения подробной информации.

_По книге [Антонио Меле: Django 2 в примерах](https://dmkpress.com/catalog/computer/programming/python/978-5-97060-746-6/)_
