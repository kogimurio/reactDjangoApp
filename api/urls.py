from django.urls import path
from .import views
from .views import PasswordResetRequestView, PasswordResetConfirmView


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<username>/', views.customUserProfile, name='profile'),
    path('product_list/', views.product_view, name='productList'),
    path('product_create/', views.product_create, name='productCreate'),
    path('product_update/<slug:slug>/', views.product_update, name='productUpdate'),
    path('product_delete/<slug:slug>/', views.product_delete, name='productDelete'),
    path('product_detail/<slug:slug>/', views.product_detail, name='productDetail'),
    path('mpesa_payment/<slug:slug>/', views.mpesa_view, name='mpesa'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset-email/', views.password_reset_email, name='password_reset_email'),
]