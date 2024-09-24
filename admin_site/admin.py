from django.contrib import admin
from .models import Product, ProductPhotos, BlogPost, PostResource, GaleryModel, About,\
    Customer, PostComments, CustomerReview, AddToCart, OrderAddress, Orders


# Model Registrations

class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]


class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductPhotos._meta.fields]


class BlogPostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductPhotos._meta.fields]


class PostResAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductPhotos._meta.fields]


class PostCommenstAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostComments._meta.fields]


class GalleryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductPhotos._meta.fields]


class AboutAdmin(admin.ModelAdmin):
    list_display = [field.name for field in About._meta.fields]


class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomerReview._meta.fields]


class AddToCartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AddToCart._meta.fields]


class OrderAddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderAddress._meta.fields]


class OrdersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Orders._meta.fields]


admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderAddress, OrderAddressAdmin)
admin.site.register(AddToCart, AddToCartAdmin)
admin.site.register(CustomerReview, CustomerReviewAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(About,AboutAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductPhotos,ProductPhotoAdmin)
admin.site.register(BlogPost)
admin.site.register(PostResource)
admin.site.register(PostComments,PostCommenstAdmin)
admin.site.register(GaleryModel)

