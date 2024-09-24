from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # tinymce url for loading tinymce js and css files
    path('tinymce/', include('tinymce.urls')),

    # restaurant site urls
    path('',include('restaurant_site.urls')),



    # admin site urls
    # home or index page
    path('admin/', views.home, name='home'),

    # orders and order details
    path('orders/', views.orders, name='orders'),
    path('undeliverable-orders/', views.undelivered_order, name='undelivered_orders'),
    path('orders/order_details/<int:id>/', views.order_details, name='order_details'),
    path('today-deliveries/', views.today_deliveries, name='today_deliveries'),

    # users and user details
    path('users/', views.users, name='users'),
    path('users/user_details/<int:id>/', views.user_details, name='user_details'),

    # products
    path('products/', views.products_list, name='products_list'),
    path('products/product_details/<int:id>/', views.product_details, name="product_details"),
    path('products/product_details/edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('products/add_product/', views.add_product, name='add_product'),

    # blog
    path('blog_posts/', views.post_list, name='post_list'),
    path('blog_posts/add_post/', views.add_post, name='add_post'),
    path('blog_posts/add_post/add_post_res/', views.add_post_res, name='add_post_res'),
    path('blog_posts/add_post/post/', views.add_post_detail, name='add_post_detail'),
    path('blog_post/post_detail/<int:id>/', views.post_details, name='post_details'),
    path('blog_posts/delete-post/<int:id>/',views.delete_post,name='delete_post'),


    # gallery
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:id>/', views.image, name='image'),


    # about
    path('admin/about/', views.about, name='about'),
    path('admin/about/<int:id>/', views.about_update, name='about_update'),

    #reports
    path('reports/', views.reports_view , name='reports')

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
