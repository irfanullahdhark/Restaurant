from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('menu/', views.menu, name='menu'),
    path('blogs/', views.blogs, name='blogs'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.user_signup, name='signup'),
    path('cart/', views.cart, name='cart'),
    path('cart/address/',views.addressing, name='address'),
    path('order-now/', views.order_now, name='order_now'),
    path('product-details/<int:id>/', views.product_details, name='pro_details'),
    path('restaurant-gallery/',views.gallery,name='site_gallery'),
    path('restaurant-gallery/<int:x>/', views.image, name='image_view'),
    path('images/<int:x>/', views.image, name='image_view'),
    path('blogs/blog-details/<int:id>/', views.blog_details, name='blog_details'),
    path('about/', views.about, name='rest_about'),
    path('login/', views.user_login, name='login'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('addresses/',views.update_address, name='update_address'),
    path('logout/', views.user_logout, name="logout"),
    path('404/', views.page_not_found,name='404')



]