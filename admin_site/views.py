from django.shortcuts import render, redirect, reverse
from .forms import ProductForm, ProductPhotosForm,PostResForm,AddPostForm, GalleryForm, AboutForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .models import Product, ProductPhotos, BlogPost, PostResource, GaleryModel, GaleryModel, Customer,\
    About, Orders, AddToCart
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
# admin section


# home page index.html

def home(request):
    recent_product = ProductPhotos.objects.order_by('-pro_id')[:4]
    now = timezone.localtime()
    two_days_ago = now - timedelta(hours=48)
    a_week_ago = now - timedelta(weeks=1)
    day_ago = now - timedelta(hours=24)

    latest_customers = Customer.objects.filter(created_at__gte=two_days_ago,created_at__lte=now,is_superuser=False).order_by('-created_at')
    new_orders = Orders.objects.filter(order_date__range=(a_week_ago, now)).order_by('-order_date')

    number_of_undelivered_orders = len(Orders.objects.filter(status='undelivered'))
    number_of_new_orders = len(new_orders)
    number_of_new_customers = len(latest_customers)
    number_of_all_customers = len(Customer.objects.all())
    number_of_today_deliveries = len(Orders.objects.filter(Q(status='delivered') & Q(order_date__range=(day_ago, now))))

    cart_products = AddToCart.objects.filter(customer=request.user)
    total_price = 0
    for product in cart_products:
        total_price += (product.product.price * product.quantity)

    context = {
        'recent_products':recent_product,
        'latest_customers': latest_customers,
        'no_latest_customers':number_of_new_customers,
        'orders': new_orders,
        'no_new_orders':number_of_new_orders,
        'no_of_undelivered_orders':number_of_undelivered_orders,
        'no_of_all_customers': number_of_all_customers,
        'no_of_today_deliveries': number_of_today_deliveries,
    }
    return render(request, 'admin/index.html',context)


# orders page listing orders
@csrf_exempt
def orders(request):
    if request.method == "POST":
        id = int(request.POST['id'])
        order = Orders.objects.get(pk=id)
        order.delete()
        all_orders = Orders.objects.all()
        data = []

        for obj in all_orders:
            ordered_products = [product.name for product in obj.ordered_products.all()]

            customer_dict = {
                'id': obj.custID.id,
                'first_name': obj.custID.first_name,
                'username': obj.custID.username,
                'phone': obj.custID.phone,
                'photo': 'no image',
                'created_at': obj.custID.created_at
            }
            order_dict = {
                'id': obj.id,
                'custID': customer_dict,
                'addID': obj.addID_id,
                'order_date': obj.order_date,
                'shipping_cost': obj.shipping_cost,
                'status': obj.status,
                'ordered_products': ordered_products,
                'subtotal': obj.subtotal,
            }
            data.append(order_dict)

        return JsonResponse({'status':'delete','all_orders': data})
    else:
        all_orders = Orders.objects.all()

    context = {
        'all_orders': all_orders,
    }
    return render(request, 'admin/pages/tables/orders.html',context)


def undelivered_order(request):
    if request.method == "POST":
        id = int(request.POST['id'])
        order = Orders.objects.get(pk=id)
        order.delete()
        undelivered_orders = Orders.objects.filter(status='undelivered')
        data = []

        for obj in undelivered_orders:
            ordered_products = [product.name for product in obj.ordered_products.all()]

            customer_dict = {
                'id': obj.custID.id,
                'first_name': obj.custID.first_name,
                'username': obj.custID.username,
                'phone': obj.custID.phone,
                'photo': 'no image',
                'created_at': obj.custID.created_at
            }
            order_dict = {
                'id': obj.id,
                'custID': customer_dict,
                'addID': obj.addID_id,
                'order_date': obj.order_date,
                'shipping_cost': obj.shipping_cost,
                'status': obj.status,
                'ordered_products': ordered_products,
                'subtotal': obj.subtotal,
            }
            data.append(order_dict)

        return JsonResponse({'status':'delete','all_orders': data})
    else:
        undelivered_orders = Orders.objects.filter(status='undelivered')

    context = {
        'orders': undelivered_orders
    }
    return render(request,'admin/pages/tables/undelivered_orders.html',context)


def today_deliveries(request):

    now = timezone.localtime()
    day_ago = now - timedelta(hours=24)
    deliveries = Orders.objects.filter(Q(status='delivered') & Q(order_date__range=(day_ago, now)))

    context = {'deliveries':deliveries}
    return render(request,'admin/pages/tables/today_deliveries.html',context)


# order details page
def order_details(request,id):
    if request.method == "POST":
        try:
            order = Orders.objects.get(pk=id)
        except ObjectDoesNotExist:
            return redirect('404')
        order.status = 'delivered'
        order.save()
        return HttpResponseRedirect('/orders/')
    else:
        try:
            order = Orders.objects.get(pk=id)
        except ObjectDoesNotExist:
            return redirect('404')
    context = {
        'order': order,
    }
    return render(request, 'admin/pages/tables/order_detail.html',context)


# users page
@csrf_exempt
def users(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search = request.POST['search']
            print(f'searched {search} -----------------------------------------')
            if search != '':
                print('search finding-----------------------------------------------')
                customers = Customer.objects.filter(Q(first_name__contains=search) & Q(is_superuser=False))
            else:
                print('search not find -----------------------------------------')
                customers = Customer.objects.filter(is_superuser=False)


        else:
            id = int(request.POST['id'])
            customer = Customer.objects.get(pk=id)
            customer.delete()

            data = []
            customers = Customer.objects.filter(is_superuser=False)

            for cust in customers:

                cust_dict = {
                    'id': cust.id,
                    'first_name': cust.first_name,
                    'username': cust.username,
                    'phone' : cust.phone,
                    'photo': cust.photo.url,
                    'created_at': cust.created_at,
                    'email': cust.email,
                }
                data.append(cust_dict)

            return JsonResponse({'status':'delete','all_customers': data})
    else:
        customers = Customer.objects.filter(is_superuser=False)

    context = {'customers':customers}
    return render(request, 'admin/pages/tables/users.html',context)


# user details page
def user_details(request,id):
    try:
        customer = Customer.objects.get(pk=id)
    except ObjectDoesNotExist:
        return redirect('404')

    orders = Orders.objects.filter(custID=customer)
    context = {
        'customer':customer,
        'orders':orders,
    }
    return render(request, 'admin/pages/tables/user_details.html',context)


# product. product operation section
# products list page
@csrf_exempt
def products_list(request):
    if request.method == "POST":
        id = int(request.POST['id'])
        category = request.POST['category']
        try:
            product = ProductPhotos.objects.get(pk=id)
        except ObjectDoesNotExist:
            return redirect('404')

        product.delete()
        if category != '':
            product_photos = ProductPhotos.objects.filter(pro_id__category=category)
        else:
            product_photos = ProductPhotos.objects.all()
        data = []
        for prodPhoto in product_photos:
            prod_dict = {
                'id': prodPhoto.pro_id.id,
                'name':prodPhoto.pro_id.name,
                'price': prodPhoto.pro_id.price,
                'old_price': prodPhoto.pro_id.old_price,
                'category': prodPhoto.pro_id.category,
                'info': prodPhoto.pro_id.info,
                'description': prodPhoto.pro_id.description,
            }
            prod_photo_dict = {
                'pro_id': prod_dict,
                'photo1': prodPhoto.photo1.url,
            }
            data.append(prod_photo_dict)

        return JsonResponse({'status': 'deleted', 'foods': data})

    all_foods = ProductPhotos.objects.all()
    pizzas = ProductPhotos.objects.filter(pro_id__category='pizza')
    beverage = ProductPhotos.objects.filter(pro_id__category='beverage')
    special_juice = ProductPhotos.objects.filter(pro_id__category='special-juice')
    sweets = ProductPhotos.objects.filter(pro_id__category='sweets')
    rice_biryani = ProductPhotos.objects.filter(pro_id__category='rice-biryani')
    fast_food = ProductPhotos.objects.filter(pro_id__category='fast-food')
    bar_be_coe = ProductPhotos.objects.filter(pro_id__category='bar-be-coe')
    salad = ProductPhotos.objects.filter(pro_id__category='salad')
    special_top = ProductPhotos.objects.filter(pro_id__category='special-top')
    afghani_special = ProductPhotos.objects.filter(pro_id__category='afghani-special')
    pakistani = ProductPhotos.objects.filter(pro_id__category='pakistani')
    chinese = ProductPhotos.objects.filter(pro_id__category='chinese')
    soup = ProductPhotos.objects.filter(pro_id__category='soup')
    fish = ProductPhotos.objects.filter(pro_id__category='fish')
    print(f'rice_biryanin {rice_biryani}----------------------------------')
    context = {
        'all_foods': all_foods,
        'pizzas': pizzas,
        'beverages': beverage,
        'special_juices': special_juice,
        'sweets': sweets,
        'rice_biryanis': rice_biryani,
        'fast_foods': fast_food,
        'bar_be_coes': bar_be_coe,
        'salads': salad,
        'special_tops': special_top,
        'afghani_specials': afghani_special,
        'pakistanis': pakistani,
        'chineses': chinese,
        'soups': soup,
        'fishes': fish,
    }
    return render(request, 'admin/pages/products/product_list.html',context)


# products detail page
def product_details(request,id):
    try:
        product = ProductPhotos.objects.get(pro_id=id)
    except ObjectDoesNotExist:
        return redirect('404')
    context = {'product':product}
    return render(request, 'admin/pages/products/product_details.html',context)


# edit product page
def edit_product(request,id):
    try:
        product_photo = ProductPhotos.objects.get(pro_id=id)
        product_photo.pro_id = Product.objects.get(pk=id)
    except ObjectDoesNotExist:
        return redirect('404')
    product = product_photo.pro_id

    if request.method == 'POST':
        prodform = ProductForm(request.POST,instance=product)
        prodphotoform = ProductPhotosForm(request.POST,request.FILES,instance=product_photo)

        if prodform.is_valid() and prodphotoform.is_valid():
            prodform.save()
            prodphotoform.save()

            return HttpResponseRedirect(reverse('product_details',args=[id]))

    else:

        prodform = ProductForm(instance=product)
        prodphotoform = ProductPhotosForm(instance=product_photo)

    context = {'prodform': prodform, 'prodphotoform': prodphotoform}
    return render(request, 'admin/pages/products/edit_product.html',context)


# add product page
def add_product(request):

    if request.method == 'POST':
        prodform = ProductForm(request.POST)
        prodphotoform = ProductPhotosForm(request.POST,request.FILES)

        print(f'product_form {prodform}')
        print(f'product photos {prodphotoform} ')

        if prodform.is_valid() and prodphotoform.is_valid():
            product = prodform.save()
            prod_photo = prodphotoform.save(commit=False)
            prod_photo.pro_id = product
            prod_photo.save()
            print('data save successfully')
            messages.add_message(request, messages.SUCCESS, 'Product Added!')
            return HttpResponseRedirect('/products/add_product/')


    else:
        prodform = ProductForm()
        prodphotoform  = ProductPhotosForm()

    context = {'prodform': prodform,'prodphotoform':prodphotoform}
    return render(request, 'admin/pages/products/add_product.html', context)


# _______________________________________________________________________________________________


# blog section
# posts list page
def post_list(request):
    if request.method == 'POST':
        if 'table_search' in request.POST:
            search_post = request.POST['table_search']
            searched_post_data = BlogPost.objects.filter(post_sub__contains=search_post).order_by('-id')
            posts = searched_post_data
            total_post = len(posts)
            paginator = Paginator(posts, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        else:
            posts = BlogPost.objects.order_by('-id')
            paginator = Paginator(posts, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            total_post = len(posts)

    else:
        posts = BlogPost.objects.order_by('-id')
        paginator = Paginator(posts,3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        total_post = len(posts)

    context = {
        'posts': page_obj,
        'total_post':total_post,
    }
    return render(request, 'admin/pages/blogs/posts_list.html',context)


# post details page
def post_details(request,id):
    try:
        post = BlogPost.objects.get(pk=id)
    except ObjectDoesNotExist:
        return redirect('404')

    context = {
        'post': post,
    }
    return render(request, 'admin/pages/blogs/post_details.html',context)


def add_post(request):
    if request.method == 'POST':
        return HttpResponseRedirect('add_post_res')
    return render(request,'admin/pages/blogs/add.html')


def add_post_detail(request):
    if request.method == 'POST':
        post_form = AddPostForm(request.POST,request.FILES)
        if post_form.is_valid():
            post_form.save()
            return HttpResponseRedirect('/blog_posts/')
    else:
        post_form = AddPostForm()
    context = {
        'post_form':post_form,
    }
    return render(request,'admin/pages/blogs/add_post.html',context)


def delete_post(request,id):
    if request.method == "POST":
        try:
            post = BlogPost.objects.get(pk=id)
        except ObjectDoesNotExist:
            return redirect('404')

        post.delete()
        return HttpResponseRedirect('/blog_posts/')


# add post
def add_post_res(request):
    if request.method == 'POST':
        post_res_form = PostResForm(request.POST, request.FILES)
        print(f'post resource {post_res_form}')
        if post_res_form.is_valid():
            print('valid')
            post_res_form.save()
            return HttpResponseRedirect('/blog_posts/add_post/')
        else:
            print('form is not valid')

    else:
        post_res_form = PostResForm()

    context = {
        'post_res_form': post_res_form,
    }
    return render(request, 'admin/pages/blogs/add_post_res.html',context)


# gallery page
def gallery(request):

    if request.method == 'POST':
        form = GalleryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            form = GalleryForm()

        data = GaleryModel.objects.all()

    else:
        form = GalleryForm()
        data = GaleryModel.objects.all()
    context = {
        'form': form,
        'data': data,
    }
    return render(request,'admin/pages/gallery.html',context)


def image(request,id):
    try:
        picture = GaleryModel.objects.get(pk=id)
    except ObjectDoesNotExist:
        return redirect('404')

    context = {'pic':picture}
    return render(request,'admin/pages/image.html',context)


def about(request):
    if request.method == "POST":
        data = About.objects.all()[:1]
        form = AboutForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()

    else:
        data = About.objects.all()
        form = AboutForm()

    context = {
        'form': form,
        'data': data
    }
    return render(request,'admin/pages/about.html',context)


def about_update(request,id):

    if request.method == "POST":
        try:
            data = About.objects.get(pk=id)
        except ObjectDoesNotExist:
            return redirect('404')

        form = AboutForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
    else:
        try:
            data = About.objects.get(pk=id)
        except ObjectDoesNotExist:
            return redirect('404')

        form = AboutForm(instance=data)

    context = {'form':form}
    return render(request,'admin/pages/about.html',context)


def reports_view(request):
    now = timezone.localtime()

    today = now - timedelta(hours=24)
    last_week = now - timedelta(hours=168)
    last_month = now - timedelta(hours=720)

    today_new_users = Customer.objects.filter(created_at__gte=today, created_at__lte=now,is_superuser=False).order_by('-created_at')
    today_orders = Orders.objects.filter(order_date__gte=today,order_date__lte=now).order_by('-id')
    today_total_orders = len((today_orders))
    today_total_sale = 0
    for order in today_orders:
        today_total_sale += order.subtotal

    weekly_new_users = Customer.objects.filter(created_at__gte=last_week, created_at__lte=now,is_superuser=False).order_by('-created_at')
    weekly_orders = Orders.objects.filter(order_date__gte=last_week,order_date__lte=now).order_by('-id')
    weekly_total_orders = len(weekly_orders)
    weekly_total_sale = 0
    for order in weekly_orders:
        weekly_total_sale += order.subtotal

    monthly_new_users = Customer.objects.filter(created_at__gte=last_month, created_at__lte=now,is_superuser=False).order_by('-created_at')
    monthly_orders = Orders.objects.filter(order_date__gte=last_month,order_date__lte=now).order_by('-id')
    monthly_total_orders = len(monthly_orders)
    monthly_total_sale = 0
    for order in monthly_orders:
        monthly_total_sale += order.subtotal

    context = {
        'today_new_user': today_new_users,
        'today_orders': today_orders,
        'today_total_orders': today_total_orders,
        'today_total_sale': today_total_sale,

        'weekly_new_users': weekly_new_users,
        'weekly_orders': weekly_orders,
        'weekly_total_orders': weekly_total_orders,
        'weekly_total_sale': weekly_total_sale,

        'monthly_new_users': monthly_new_users,
        'monthly_orders': monthly_orders,
        'monthly_total_orders': monthly_total_orders,
        'monthly_total_sale': monthly_total_sale,


    }
    return render(request,'admin/pages/report/reports.html',context=context)

