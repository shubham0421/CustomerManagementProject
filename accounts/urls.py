from django.urls import path

from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('user/', views.userPage, name="user-page"),
    path('', views.home, name="home"),
    path('account/', views.accountSettings, name="account"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk_test>/', views.customer, name='customer'),
    path('create_order/<str:pk>/',views.createorder,name='create_order'),
    path('update_order/<str:pk>/',views.updateorder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteorder,name='delete_order')


    




]
