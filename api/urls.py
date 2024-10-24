from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product_list/', views.product_view, name='productList'),
    path('product_create/', views.product_create, name='productCreate'),
    path('product_update/<slug:slug>/', views.product_update, name='productUpdate'),
    path('product_delete/<slug:slug>/', views.product_delete, name='productDelete'),
    path('product_detail/<slug:slug>/', views.product_detail, name='productDetail'),
]