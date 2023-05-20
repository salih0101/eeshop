from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('category/<int:pk>/', views.get_exact_category),
    path('item/<int:pk>', views.exact_product),
    path('basket',views.get_Basket),
    path("order", views.complete_order)



]