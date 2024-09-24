from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField


class Customer(AbstractUser):
    first_name = models.CharField(max_length=150)
    username = models.CharField(max_length=254, unique=True)
    phone = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='image/')
    created_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.first_name


class Product(models.Model):

    cat_choices = (
        ('pizza', 'pizza'),
        ('beverage', 'beverage'),
        ('special juice', 'special juice'),
        ('sweets', 'sweets'),
        ('rice-biryani', 'rice-biryani'),
        ('fast-food', 'fast-food'),
        ('bar-be-coe', 'bar-be-coe'),
        ('salad', 'salad'),
        ('special-top', 'special-top'),
        ('afghani-special', 'afghani-special'),
        ('pakistani', 'pakistani'),
        ('chinese', 'chinese'),
        ('soup', 'soup'),
        ('fish', 'fish'),

    )

    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField(null=True)
    category = models.CharField(choices=cat_choices, max_length=64)
    info = models.TextField()
    description = HTMLField()

    def __str__(self):
        return self.name


class ProductPhotos(models.Model):
    pro_id = models.OneToOneField(Product, on_delete=models.CASCADE, unique=True,related_name='product_photos')
    photo1 = models.ImageField(upload_to='admin/product/img/')
    photo2 = models.ImageField(upload_to='admin/product/img/', null=True)
    photo3 = models.ImageField(upload_to='admin/product/img/', null=True)
    photo4 = models.ImageField(upload_to='admin/product/img/', null=True)
    photo5 = models.ImageField(upload_to='admin/product/img/', null=True)
    photo6 = models.ImageField(upload_to='admin/product/img/')

    def __str__(self):
        return str(self.pro_id)


class CustomerReview(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    comnt_data = models.DateField(auto_now=True)
    comment = models.TextField()

    def __str__(self):
        return self.customer_id


class AddToCart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('product', 'customer')


class PostResource(models.Model):
    res_name = models.CharField(max_length=254,unique=True)
    res_img = models.ImageField(upload_to='admin/blog/resources/img/')
    res_info = HTMLField()

    def __str__(self):
        return self.res_name


class BlogPost(models.Model):

    post_res = models.ForeignKey(PostResource,on_delete=models.CASCADE)
    post_author = models.CharField(max_length=254)
    post_sub = models.TextField()
    post_img = models.ImageField(upload_to='admin/blog/img/')
    post_desc = HTMLField();
    post_date = models.DateField(auto_now=True)
    

    def __str__(self):
        return self.post_sub


class PostComments(models.Model):
    postid = models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='post_comment')
    cust_name = models.CharField(max_length=164)
    cust_img = models.ImageField(upload_to='admin/blog/comment/')
    message = models.TextField()

    def __str__(self):
        return self.user_name


# gallery
class GaleryModel(models.Model):
    title = models.CharField(max_length=254,null=True)
    image = models.ImageField(upload_to='admin/restaurant_images/')

    def __str__(self):
        return self.title


class About(models.Model):
    name = models.CharField(max_length=254,unique=True)
    picture = models.ImageField(upload_to='user/about/')
    info = HTMLField()
    story =HTMLField()


class OrderAddress(models.Model):
    area_choices = (
        ('first area', '1st Area'),
        ('second area', '2nd Area'),
        ('third area', '3rd Area'),
        ('fourth area', '4th Area'),
        ('fifth area', '5th Area'),
        ('sixth area', '6th Area'),
        ('seventh area', '7th Area'),
        ('eighth area', '8th Area'),
        ('ninth area', '9th Area'),
        ('tenth area', '10th Area'),
        ('eleventh area', '11th Area'),
        ('twelfth  area', '12th Area'),
        ('thirteenth  area', '13th Area'),
        ('fourteenth  area', '14th Area'),
        ('fifteenth  area', '15th Area'),
        ('sixteenth  area', '16th Area'),
    )
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='customer_address')
    area = models.CharField(choices=area_choices,max_length=128)
    street = models.CharField(max_length=254)
    shop_home = models.CharField(max_length=200)
    address = models.CharField(max_length=254)
    phone = models.CharField(max_length=13)
    order_note = models.TextField()
    current_address = models.BooleanField()

    def __str__(self):
        return self.area


class Orders(models.Model):
    status_choices = (
        ('delivered','delivered'),
        ('undelivered','undelivered')
    )
    custID = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='cust_orders')
    addID = models.OneToOneField(OrderAddress,on_delete=models.CASCADE,related_name='address_of_order')
    order_date = models.DateTimeField(auto_now=True)
    shipping_cost = models.PositiveIntegerField()
    status = models.CharField(max_length=15,choices=status_choices)
    ordered_products = models.ManyToManyField(Product)
    subtotal = models.IntegerField()

    def __str__(self):
        return str(self.id)






