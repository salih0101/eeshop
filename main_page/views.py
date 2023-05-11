from django.shortcuts import render, redirect
from . import models
from .forms import SearchForm
from .models import Product
from telebot import TeleBot

bot = TeleBot('6078879739:AAFr51aQW09DdbaeL31Ez3iyKpjAy1A-etg', parse_mode='HTML')



def index(request):
    # Берем все категории с база данных
    all_categories = models.Category.objects.all()
    all_products = models.Product.objects.all()

    search_bar = SearchForm()

    # Создаем словарь
    context = {'all_categories': all_categories,
               'products': all_products,
               'form': search_bar}

    if request.method == 'POST':
        product_find = request.POST.get('search_product')
        try:
            search_result = Product.objects.get(product_name=product_find)
            return redirect(f'/item/{search_result.id}')
        except:
            return redirect('/')

    # Передаем на фронт
    return render(request, 'index.html', context)


def current_category(request, pk):
    category = models.Category.objects.get(id=pk)
    context = {'products', category}

    return render(request, 'current_category.html', context)


def get_exact_category(request, pk):
    # poluchaem categorii
    exact_category = models.Category.objects.get(id=pk)
    categories = models.Category.objects.all()

    # vivodim product iz etoy categorii
    category_products = models.Product.objects.filter(product_category=exact_category)

    return render(request, 'categrory_products.html', {'category_products': category_products,
                                                       'categories': categories})

def get_exact_product(request,pk):
    product = models.Product.objects.get(id=pk)
    context = {'product': product}

    if request.method == 'POST':

        models.UserCart.objects.create(user_id=request.user.id,
                                       product=product,
                                       quantity=request.POST.get('quantity'),
                                       total_for_product = product.product_price*int(request.POST.get('quantity')))
        return redirect('/cart')

    return render(request, 'about_product.html', context)


# Получить определенный продукт
def get_user_cart(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    total = sum([i.total_for_product for i in user_cart])
    context = {'cart': user_cart,
               'total': total}

    return render(request, 'user_cart.html', context)


def complete_order(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    result_message = 'Новый заказ(Сайт)\n\n'
    total_for_all_cart = 0

    for cart in user_cart:
        result_message += f'<b>{cart.product}</b> x {cart.quantity} = {cart.total_for_product} сум\n'

        total_for_all_cart += cart.total_for_product

    result_message += f'\n----------\n<b>Итого: {total_for_all_cart}сум</b>'

    #Отправляем админу сообщения
    bot.send_message(1186132006, result_message)

    return redirect('/')


