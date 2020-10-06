# Интернет магазин

Интернет-магазин c  каталогом товаров, корзиной и возможностью оформления заказов. 

### Основной функционал:
- каталог товаров пополняемый через админку;
- формирование корзины товаров. Корзина реализована с помощью `сессий Django`;
- в админке магазина динамически формируются счета в `PDF`;
- упарвление и выгрузка заказов в `CSV`;
- после создания заказа  на электронную почту пользователей отправляется `pdf-счет` в асинхронном режиме через `Celery`;
- реализована система скидок (купонов) и рекомендация товаров с помощью `Redis`.


## Установка
Эти инструкции помогут вам создать копию проекта и запустить ее на локальном компьютере для целей разработки и тестирования.

### Запуск проекта (на примере Linux)

Перед тем, как начать: если вы не пользуетесь `Python 3`, вам нужно будет установить инструмент `virtualenv` при помощи `pip install virtualenv`. 
Если вы используете `Python 3`, у вас уже должен быть модуль [venv](https://docs.python.org/3/library/venv.html), установленный в стандартной библиотеке.

- Создайте на своем компютере папку проекта `mkdir myshop` и перейдите в нее `cd myshop`
- Склонируйте этот репозиторий в текущую папку `git clone https://github.com/SergePogorelov/myshop.git .`
- Создайте виртуальное окружение `python3 -m venv venv`
- Установите зависимости `pip install -r requirements.txt`
- Накатите миграции `python manage.py migrate`
- Создайте суперпользователя Django `python manage.py createsuperuser --username admin --email 'admin@example.com'`
- Запустите сервер разработки Django `python manage.py runserver`

## В разработке использованы

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Sorl-thumbnail](https://pypi.org/project/sorl-thumbnail/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryproject.org/en/stable/)
- [RabbitMQ](https://www.rabbitmq.com/)

