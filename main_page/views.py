from django.shortcuts import render, redirect
from .models import Category, Product, Basket
from .forms import SearchForm
from telebot import TeleBot

bot= TeleBot('6293838747:AAHNdCHq943pNOBm2IHpTozwvc4yaj7Sxbo', parse_mode="HTML")
def index(request):
    #Берем все категории с базы данных
    all_categories = Category.objects.all()
    all_products = Product.objects.all()
    search_bar = SearchForm()


    context = {'all_categories': all_categories, 'all_products': all_products,"form":search_bar}

    if request.method == "POST":
        product_find = request.POST.get('search_product')
        try:
            search_result = Product.objects.get(product_name = product_find)
            return redirect(f'/item/{search_result.id}')
        except:
               return redirect('/')
    return render(request,'index.html', context)

    # # Получаем значение введенное в поисковую строку на сайте
    # from_front= request.GET.get('exact_product')
    #
    # # Было ли введено что-то в поиске
    # if from_front is not None:
    #     all_products = models.Product.objects.filter(product_name__contains = from_front)

    #Создаем словарь
    # context = {'all_categories': all_categories,'all_products': all_products}



    # Передаем на фронт
    # return render(request,'index.html', context)


def current_category(request, pk):
    category = Product.objects.get(id=pk)

    context = {'products': category}

    return render(request, 'current_category.html', context)

def get_exact_category(request, pk):
    # Получаем категорию
    exact_category = Category.objects.get(id= pk)
    categories = Category.objects.all()
    # Выводим продукты с этой категории
    category_products = Product.objects.filter(product_category=exact_category)

    return render(request, 'categrory_products.html', {'category_products': category_products, "categories" : categories})


# Получить определенный продукт
def exact_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    if request.method == "POST":
        Basket.objects.create(user_id = request.user.id,
                              user_product= product,
                              user_product_quantity= request.POST.get("user_product_quantity"),
                              total_for_product=product.product_price*int(request.POST.get('user_product_quantity')))
        return redirect('/basket')

    return render(request, 'about_product.html', context)

def get_Basket(request):
    basket = Basket.objects.filter(user_id = request.user.id)
    total = sum([i.total_for_product for i in basket])
    return render(request, 'user_cart.html', {'cart': basket, "total":total})


def complete_order(request):
    #получвем корзину пользователя по айди пользователя
    user_cart = Basket.objects.filter(user_id = request.user.id)
    # формируем сообщения для тг админа
    result_message = 'Новый заказ(сайт)\n\n'
    total_for_all_cart=0
    for cart in user_cart:
        result_message += f'<b>{cart.user_product}</b> x {cart.user_product_quantity} = {cart.total_for_product} сум\n'
        total_for_all_cart += cart.total_for_product

    result_message += f'\n----------\n<b>ИТОГО: {total_for_all_cart}сум</b>'
    #Отправляем админу сообщение в тг
    bot.send_message(1186132006, result_message)
    user_cart.delete()
    return redirect('/')


