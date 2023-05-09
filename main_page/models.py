from django.db import models


# Create your models here.

# Создать таблицу категорий
class Category(models.Model):
    category_name = models.CharField(max_length=75)
    reg_date = models.DateTimeField(auto_now_add=True)

    # Вывод информации в нормальном виде
    def __str__(self):
        return self.category_name


# Создать таблицу для продуктов
class Product(models.Model):
    # Создаем колонки для таблицы продуктов
    product_name = models.CharField(max_length=125)
    product_count = models.IntegerField()
    product_price = models.FloatField()
    product_photo = models.ImageField(upload_to='media')
    product_des = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    reg_date = models.DateTimeField(auto_now_add=True)

    # Вывод информации в нормальном виде
    def __str__(self):
        return self.product_name

# Создать корзину для продуктов
class UserCart(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_for_product = models.FloatField()

    # def __str__(self):
    #     return str(f"{self.quantity} x {self.product.name} = {self.total_for_product}")

    def __str__(self):
        return str(self.product)

    