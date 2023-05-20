from django.db import models

# Создаем таблицу категорий
class Category(models.Model):
    # Создаем колонки для таблицы
    category_name = models.CharField(max_length=75)# Категория с именами до 75 символов
    reg_data = models.DateTimeField(auto_now_add=True)# Добавляем дату и время

    #Выводим информацию в нормальном виде
    def __str__(self):
        return self.category_name

# Создаем таблицу для продукта
class Product(models.Model):
    # Создаем колонки для таблицы продуктов
    product_name = models.CharField(max_length=125) #Создаем категорию с именами
    product_count = models.IntegerField() #Создаем категорию с количеством
    product_price = models.FloatField() #Создаем категорию с ценой
    product_photo = models.ImageField(upload_to='media') #Создаем категорию с фото
    product_des = models.TextField() #Создаем категорию с описанием
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE) #прописали вызов категории и удаление товара

    reg_date = models.DateTimeField(auto_now_add=True) #Создаем категорию с датой и временем


    #Вывод в нормальный виде
    def __str__(self):
        return self.product_name


class Basket(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_product_quantity = models.IntegerField()
    total_for_product = models.FloatField()


    def __str__(self):
        return str(self.user_product)