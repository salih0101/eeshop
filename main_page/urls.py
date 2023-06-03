from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('category/<int:pk>/', views.get_exact_category),
    path('item/<int:pk>', views.exact_product),
    path('del_item/<int:pk>', views.delete_pr_from_cart),
    path('basket',views.get_Basket),
    path("order", views.complete_order)



]