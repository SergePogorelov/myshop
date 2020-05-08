import redis
from django.conf import settings

from .models import Product


r = redis.StrictRedis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
    )


class Recommender(object):

    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def product_bought(self, products):
        products_id = [p.id for p in products]
        for product_id in products_id:
            for with_id in products_id:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_result=6):
        """
        В этой функции мы выполняем следующие действия:
            1) получаем идентификаторы переданных объектов;
            2)	если переданный в качестве аргумента список товаров содержит един-
        ственное значение, сразу получаем список товаров, купленных с ним,
        при этом учитывая их рейтинг. Для этого используем команду Redis,
        ZRANGE. Ограничиваем результат максимальным количеством, max_results,
        который по умолчанию равен 6;
            3)	если в списке – аргументе функции задано более одного товара, форми-
        руем временный ключ для Redis, используя идентификаторы товаров;
            4)	суммируем рейтинги для каждого товара, который был куплен вместе
        с каким-либо из переданных в аргументе. Для этого обращаемся к ко-
        манде ZUNIONSTORE. Она выполняет объединение множеств по указанным
        ключам и сохраняет в Redis агрегированное значение по новому ключу.
        Более подробно об этой команде можно прочесть на странице 
        https://redis.io/commands/ZUNIONSTORE. Сохраняем результат суммирования во
        временном ключе, который генерировали на предыдущем шаге;
            5)	чтобы товары, которые были переданы в функцию в списке products, не
        попали в рекомендации, удаляем их с помощью команды ZREM;
            6)	затем получаем идентификаторы всех товаров по временному ключу,
        сортируя их командой ZRANGE. Ограничиваем результат в соответствии
        с переменной max_results. Удаляем из хранилища временный ключ;
            7)	наконец, получаем объекты Product по вычисленным на предыдущих ша-
        гах идентификаторам.
        """
        products_id = [p.id for p in products] #[12, 33, 4]
        if len(products_id) == 1:
            suggestions = r.zrange(
                self.get_product_key(products_id[0]),
                0, -1, desc=True
            )[:max_result]
        else:
            # Формируем временный ключ хранилища
            flat_ids = '_'.join([str(id) for id in products_id])
            tmp_key = f'tmp_{flat_ids}' #tmp_12_33_4
            
            # Передано несколько товаров, суммируем рейтинги их рекомендаций.
            # Сохраняем суммы во временном ключе.
            keys = [self.get_product_key(id) for id in products_id] #['product:{12}:purchased_with', 'product:{33}:purchased_with', 'product:{4}:purchased_with'
            r.zunionstore(tmp_key, keys) # Товары, которые купили вместе с {keys}
            
            # Удаляем ID товаров, которые были переданы в списке.
            r.zrem(tmp_key, *products_id) #удаляем дубли товаров (что бы в список не попали товары, которые переданы ( в корзине или со страницы товара)
            
            # Получаем товары, отсортированные по рейтингу.
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_result] #IDs товаров, купленных вместе с товарами из ID ключей - {keys}
            
            # Удаляем временный ключ.
            r.delete(tmp_key)

        suggest_products_ids = [int(id) for id in suggestions]

        # Получаем рекомендуемые товары и сортируем их.
        suggested_products = list(Product.objects.filter(id__in=suggest_products_ids))
        suggested_products.sort(key=lambda x: suggest_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.value_list('id', flat=True):
            r.delete(self.get_product_key(id))
