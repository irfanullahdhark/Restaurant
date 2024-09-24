from django.shortcuts import render, reverse, redirect
from admin_site.models import ProductPhotos, Product, GaleryModel, BlogPost, About, Customer,\
    PostResource, PostComments, CustomerReview, AddToCart, Orders, OrderAddress
from django.contrib.auth.hashers import make_password
from .forms import CustomerForm, CustomerAuthentication, PostCommentsForm, ContactForm,\
    CustomerReviewForm, AddToCartForm, OrderAddressForm, AddressAreaForm, AddressUpdateForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .utils import send_email_to_admin
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models.functions import Concat, Cast
from django.db.models import Value, URLField, Q
from django.contrib.sites.shortcuts import get_current_site
from .context_processors import custom_data
from datetime import datetime
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    products = ProductPhotos.objects.all()[:16]
    photos = GaleryModel.objects.all()
    posts = BlogPost.objects.order_by('-id')[:3]

    pizza = ProductPhotos.objects.filter(pro_id__category='pizza')[:8]
    beverage = ProductPhotos.objects.filter(pro_id__category='beverage')[:8]
    fast_food = ProductPhotos.objects.filter(pro_id__category='fast-food')[:8]
    bar_be_coe = ProductPhotos.objects.filter(pro_id__category='bar-be-coe')[:8]
    afghani_special = ProductPhotos.objects.filter(pro_id__category='afghani-special')[:8]
    pakistani = ProductPhotos.objects.filter(pro_id__category='pakistani')[:8]
    chinese = ProductPhotos.objects.filter(pro_id__category='chinese')[:8]
    rice_biryani = ProductPhotos.objects.filter(pro_id__category='rice-biryani')[:8]
    cust_review = CustomerReview.objects.order_by('-id')[:3]

    pizza_queryset = pizza[:1]
    rice_biryani_queryset = ProductPhotos.objects.filter(pro_id__category='rice-biryani')
    bar_be_coe_queryset = ProductPhotos.objects.filter(pro_id__category='bar-be-coe')[:1]

    special_pizza = pizza_queryset[0] if pizza_queryset.exists() else None
    special_rice_biryani = rice_biryani_queryset[0] if rice_biryani_queryset.exists() else None
    special_bar_be_coe = bar_be_coe_queryset[0] if bar_be_coe_queryset.exists() else None

    special = []
    if special_pizza:
        special.append(special_pizza)
    if special_rice_biryani:
        special.append(special_rice_biryani)
    if special_bar_be_coe:
        special.append(special_bar_be_coe)

    about1 = About.objects.all()[:1]
    print(f'spcecials {about1}__________________________________________')
    context = {
        'photos': photos,
        'posts': posts,
        'all_products': products,
        'specials': special,
        'about': about1,
        'cust_review': cust_review,

        'beverage': beverage,
        'rice_biryani':rice_biryani,
        'pizza': pizza,
        'fast_food': fast_food,
        'bar_be_coe': bar_be_coe,
        'afghani_special': afghani_special,
        'pakistani': pakistani,
        'chinese': chinese,

    }
    return render(request,'restaurant/index.html',context)


def menu(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search_value = request.POST['search_value']
            search_product = ProductPhotos.objects.filter(pro_id__name__contains=search_value)

        else:
            return HttpResponseRedirect('/menu/')
    else:
        search_product = []

    numberof_serached_values = len(search_product)

    all_products = ProductPhotos.objects.all()[:24]
    pizzas = ProductPhotos.objects.filter(pro_id__category='pizza')
    beverage = ProductPhotos.objects.filter(pro_id__category='beverage')
    fast_food = ProductPhotos.objects.filter(pro_id__category='fast-food')
    bar_be_coe = ProductPhotos.objects.filter(pro_id__category='bar-be-coe')
    afghani_special = ProductPhotos.objects.filter(pro_id__category='afghani-special')
    pakistani = ProductPhotos.objects.filter(pro_id__category='pakistani')
    chinese = ProductPhotos.objects.filter(pro_id__category='chinese')
    rice_biryani = ProductPhotos.objects.filter(pro_id__category='rice-biryani')
    fish = ProductPhotos.objects.filter(pro_id__category='fish')
    special_juice = ProductPhotos.objects.filter(pro_id__category='special juice')
    special_top = ProductPhotos.objects.filter(pro_id__category='special-top')
    soup = ProductPhotos.objects.filter(pro_id__category='soup')
    sweets = ProductPhotos.objects.filter(pro_id__category='sweets')
    salad = ProductPhotos.objects.filter(pro_id__category='salad')

    context = {
        'search_products': search_product,
        'total_searched': numberof_serached_values,
        'all_products': all_products,
        'pizza': pizzas,
        'beverage': beverage,
        'rice_biryani': rice_biryani,
        'fast_food': fast_food,
        'bar_be_coe': bar_be_coe,
        'afghani_special': afghani_special,
        'pakistani': pakistani,
        'chinese': chinese,
        'fish': fish,
        'special_juice': special_juice,
        'special_top': special_top,
        'soup': soup,
        'sweets': sweets,
        'salad': salad,
    }
    return render(request, 'restaurant/menu.html', context)


def blogs(request):
    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST['search']
            all_posts = BlogPost.objects.filter(post_sub__contains=search).order_by('-id')
            paginator = Paginator(all_posts, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            messages.add_message(request,messages.INFO,f'total searched posts are {len(all_posts)}')
    else:
        all_posts = BlogPost.objects.order_by('-id')
        paginator = Paginator(all_posts,6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    recent_posts = BlogPost.objects.order_by('-id')[:4]

    context = {'posts': page_obj, 'recent_posts': recent_posts}
    return render(request, 'restaurant/blog.html', context)


def blog_details(request,id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostCommentsForm(request.POST)
            if form.is_valid():
                cust_name = request.user.first_name
                cust_img = request.user.photo
                try:
                    post = BlogPost.objects.get(pk=id)
                except ObjectDoesNotExist:
                    return redirect('404')

                postcomment = form.save(commit=False)
                postcomment.cust_name = cust_name
                postcomment.cust_img = cust_img
                postcomment.postid = post
                postcomment.save()
                print('data successfully saved')
                form = PostCommentsForm()
        else:
            messages.add_message(request,messages.WARNING, 'Please first login into your account.')
            return HttpResponseRedirect('/login/')

    else:
        form = PostCommentsForm()
    try:
        post = BlogPost.objects.get(pk=id)
    except ObjectDoesNotExist:
        return redirect('404')
    post_comments = PostComments.objects.filter(postid=post)
    number_of_post_comments = len(post_comments)
    context = {'form': form, 'post': post, 'post_comments': post_comments,'number_of_post_comments':number_of_post_comments}
    return render(request,'restaurant/blog-detail.html',context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            from_email = request.POST.get('email', "")
            subject = form.cleaned_data['subject']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            if subject and message and from_email:
                try:
                    send_email_to_admin(subject=subject,message=message,phone=phone,sender_email=from_email)
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                    form = ContactForm()
            else:
                # In reality we'd use a form class
                # to get proper validation errors.
                return HttpResponse("Make sure all fields are entered and valid.")

            # send_email_to_admin(subject=subject,message=message,phone=phone,recip=recipient_mail,sender_email=sender_email)


        else:
            print('form is not valid------------------')
    else:
        form = ContactForm()
    return render(request,'restaurant/contact.html',{'form':form})


def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomerForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.password = make_password(request.POST['password1'])
                user.save()
                login(request,user)
                print('customer has saved')
                return HttpResponseRedirect(reverse('profile',args=[user.id]))
            else:
                print('form is not valid')
        else:
            form = CustomerForm()
        return render(request, 'restaurant/signup.html', {"form": form})
    else:
        return HttpResponseRedirect('/profile/')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomerAuthentication(request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    if not request.user.is_superuser:
                        return HttpResponseRedirect(reverse('profile',args=[user.id]))
                    else:
                        return HttpResponseRedirect('/admin/')

            else:
                messages.add_message(request, messages.ERROR,
                                     'Invalid username or password! please enter valid credentials')
                print(f' form is not valid')

        else:
            form = CustomerAuthentication(request)
        context = {
            'form': form
        }
        return render(request,'restaurant/login.html',context)
    else:
        return HttpResponseRedirect('/profile/')


@login_required
def profile(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(f'request data {request.POST}----------------------------------------------')
            try:
                current_user = Customer.objects.get(pk=id)
                if current_user != request.user:
                    return redirect('404')
            except ObjectDoesNotExist:
                return redirect('404')
            account_detail = CustomerForm(request.POST,request.FILES,instance=current_user)
            if request.POST['username'] == current_user.username:
                account_detail.exclude_fields(['username'])

            if account_detail.is_valid():
                user = account_detail.save(commit=False)
                user.password = make_password(request.POST['password1'])
                user.save()
                if request.POST['username'] == current_user.username:
                    current_user = user
                    account_detail = CustomerForm(instance=current_user)

                login(request, user)
                try:
                    return HttpResponseRedirect(reverse('profile', args=[user.id]))
                except:
                    print('error message goes here')
            else:
                print('account is not validate')
        else:
            try:
                current_user = Customer.objects.get(pk=id)
                if current_user != request.user:
                    return redirect('404')

            except ObjectDoesNotExist:
                return redirect('404')

            account_detail = CustomerForm(instance=current_user)

        orders = Orders.objects.filter(custID=request.user)
        last_order = Orders.objects.filter(custID=request.user)[:1]
        last_order = last_order[0] if last_order.exists() else None
        addresses = OrderAddress.objects.filter(customer=request.user).order_by('-id')
        addresses_forms = []
        for address in addresses:
            address_form = AddressUpdateForm(instance=address)
            addresses_forms.append(address_form)

        context = {
            'user': current_user,
            'account_detail': account_detail,
            'last_order': last_order,
            'orders': orders,
            'addresses_form': addresses_forms,
        }
        return render(request,'restaurant/profile.html', context)
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def update_address(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            uid = request.user.id
            if 'id' in request.POST:
                print(f'request address {request.POST}-------------------------------------------')
                id = int(request.POST['id'])
                obj = OrderAddress.objects.get(pk=id)
                form = AddressUpdateForm(request.POST,instance=obj)

                if form.is_valid():
                    order_address = form.save(commit=False)
                    check = form.cleaned_data['current_address']
                    addresses = OrderAddress.objects.filter(customer=request.user)
                    if check:
                        for address in addresses:
                            address.current_address = False
                            address.save()
                        order_address.current_address = True
                    else:
                        for address in addresses:
                            if address.current_address:
                                address.current_address = True
                            else:
                                address.current_address = False
                            address.save()
                        order_address.current_address = False
                    order_address.save()
                    orders = OrderAddress.objects.filter(customer=request.user).values('id','phone', 'area', 'street', 'shop_home', 'address','current_address').order_by('-id')
                    return JsonResponse({'status': 'save', 'orders': list(orders)})
                else:
                    print('address form is not valid')

                addresses = OrderAddress.objects.filter(customer=request.user)
                print(f'all orders {addresses[3].street}--------------------------------------------')

                return HttpResponseRedirect(f'/profile/{uid}/')
    else:
        return HttpResponseRedirect('/login/')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
def cart(request):
    if request.user.is_authenticated:
        sub_total = 0
        if request.method == "POST":

            print(f'request data {request.POST}')
            form = AddToCartForm(request.POST)

            if 'qty[]' in request.POST:
                card_products = AddToCart.objects.filter(customer=request.user)
                product_quantities = request.POST.getlist('qty[]')
                for i in range(len(card_products)):
                    card_products[i].quantity = int(product_quantities[i])
                    card_products[i].save()
                    custom_data(request)

                cart_products = AddToCart.objects.filter(customer=request.user)
                for product in cart_products:
                    sub_total += (product.quantity * product.product.price)

                current_site = get_current_site(request)
                domain = current_site.domain
                card_products = AddToCart.objects.filter(customer=request.user).annotate(
                    image_url =Cast(Concat('product__product_photos__photo1',Value('')),output_field=URLField())
                ).values('quantity','product__id','product__price','product__name','image_url')

                for data in card_products:
                    if data['image_url'] :
                        data['image_url'] = f'http://{domain}/media/{data["image_url"]}'

                return JsonResponse({'status':'save','subtotal':sub_total,'products':list(card_products)})

            if 'id' in request.POST:
                id = int(request.POST['id'])
                product = AddToCart.objects.get(pk=id)
                product.delete()

                cart_products = AddToCart.objects.filter(customer=request.user)
                for product in cart_products:
                    sub_total += (product.quantity * product.product.price)

                current_site = get_current_site(request)
                domain = current_site.domain
                card_products = AddToCart.objects.filter(customer=request.user).annotate(
                    image_url=Cast(Concat('product__product_photos__photo1', Value('')), output_field=URLField())
                ).values('id','quantity', 'product__id', 'product__price', 'product__name', 'image_url')

                for data in card_products:
                    if data['image_url']:
                        data['image_url'] = f'http://{domain}/media/{data["image_url"]}'

                return JsonResponse({'status': 'save','subtotal':sub_total, 'products': list(card_products)})


            if form:
                if form.is_valid():
                    pro_id = int(request.POST['pro_id'])
                    customer = request.user
                    product = ProductPhotos.objects.get(pk=pro_id)
                    product = product.pro_id

                    cartdata = form.save(commit=False)
                    cartdata.product = product
                    cartdata.customer = customer
                    try:
                        cartdata.save()
                    except IntegrityError:
                        return HttpResponseRedirect('/cart/')

                    cart_products = AddToCart.objects.filter(customer=request.user)
                    cart_products = AddToCart.objects.filter(customer=request.user)
                    for product in cart_products:
                        sub_total += (product.quantity * product.product.price)

                else:
                    print('form is not valid...............................')
        else:
            cart_products = AddToCart.objects.filter(customer=request.user)
            for product in cart_products:
                sub_total += (product.quantity * product.product.price)

        area_form = AddressAreaForm()
        context = {'cart_products': cart_products,'sub_total':sub_total, 'area_form': area_form}
        return render(request,'restaurant/cart.html', context)
    else:
        return HttpResponseRedirect('/login/')


area_value = ''


def addressing(request):
    if request.user.is_authenticated:
        global area_value
        if request.method == "POST":
            check_cart = AddToCart.objects.filter(customer=request.user)
            if check_cart:
                area_value = request.POST['area']
                if 'street' not in request.POST:
                    if area_value:
                        try:
                            addresses = OrderAddress.objects.get(customer=request.user, current_address=True)

                            if addresses.area != area_value:
                                address_form = OrderAddressForm(initial={'area':area_value})
                            else:
                                area = addresses.area
                                street = addresses.street
                                shop_home_no = addresses.shop_home
                                address = addresses.address
                                phone = addresses.phone
                                address_form = OrderAddressForm(initial={
                                    'area': area,'street':street,'shop_home':shop_home_no,
                                    'address':address,'phone':phone
                                })
                        except:
                            address_form = OrderAddressForm(initial={'area': area_value})

                    else:
                        messages.add_message(request,messages.ERROR,'Please Select Your Area')
                        return HttpResponseRedirect('/cart/')

                else:
                    address_form = OrderAddressForm(request.POST)
                    if address_form.is_valid():
                        cur_address = address_form.save(commit=False)
                        cur_address.customer = request.user

                        addresses = OrderAddress.objects.filter(customer=request.user)

                        for address in addresses:
                            address.current_address = False
                            address.save()

                        cur_address.current_address = True
                        cur_address.save()

                        cart_products = AddToCart.objects.filter(customer=request.user)
                        total_price = 0
                        for product in cart_products:
                            total_price += (product.product.price * product.quantity)

                        order = Orders(custID=request.user,addID=cur_address,order_date=datetime.now(),shipping_cost=0,status='undelivered',subtotal=total_price)
                        order.save()
                        products = AddToCart.objects.filter(customer=request.user)
                        for prod in products:
                            order.ordered_products.add(prod.product)

                        for prod in products:
                            prod.delete()

                        return HttpResponseRedirect(f'/profile/{request.user.id}/')
                        print(f'last part of the address ------------------------------')
                    address_form = OrderAddressForm(initial={'area':area_value})
            else:
                messages.add_message(request,messages.WARNING,'Before Proceed To Address Please Add Product In Your Cart.')
                return HttpResponseRedirect('/cart/')


        else:
            address_form = OrderAddressForm(initial={'area':area_value})

        cart_products = AddToCart.objects.filter(customer=request.user)
        total_price = 0
        for product in cart_products:
            total_price += (product.product.price * product.quantity)
        context = {'form':address_form, 'cart_products': cart_products, 'total_price':total_price,'order_date':datetime.now()}
        return render(request,'restaurant/address.html',context)

    else:
        return HttpResponseRedirect('/login/')


def order_now(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search_value = request.POST['search_value']
            if search_value != "":
                search_product = ProductPhotos.objects.filter(pro_id__name__contains=search_value)
            else:
                search_product = []
                products = ProductPhotos.objects.order_by('-id')[:16]
        else:
            return HttpResponseRedirect('/menu/')
    else:
        search_product = []

    products = ProductPhotos.objects.order_by('-id')[:16]

    context = {
        'products': products,
        'searched_products': search_product
    }
    return render(request,'restaurant/shop-categories.html', context)


def product_details(request,id):
    try:
        product = ProductPhotos.objects.get(pk=id)
    except ObjectDoesNotExist:
        return redirect('404')

    if request.method == "POST" :
        form = CustomerReviewForm(request.POST)
        if form.is_valid():
            customerid = request.user
            productid = product.pro_id

            review = form.save(commit=False)
            review.product_id = productid
            review.customer_id = customerid

            review.save()
            print('data saved successfully')

        else:
            print('form is not valid ....................')
    else:
        form = CustomerReviewForm()

    prod = ProductPhotos.objects.get(pk=id)
    related_category = prod.pro_id.category
    related_products = ProductPhotos.objects.filter(Q(pro_id__category=related_category))[:4]

    cart_form = AddToCartForm()
    try:
        cust_reviews = CustomerReview.objects.filter(product_id__id=id)
    except ObjectDoesNotExist:
        return redirect('404')
    context = {
        'product': product,
        'form': form,
        'customer_reviews': cust_reviews,
        'cart_form': cart_form,
        'related_products': related_products,
    }
    return render(request,'restaurant/product_details.html',context)


def gallery(request):
    photos = GaleryModel.objects.all()

    context = {
        'photos': photos
    }
    return render(request,'restaurant/gallery.html',context)


def image(request, x):
    try:
        picture = GaleryModel.objects.get(pk=x)
    except ObjectDoesNotExist:
        return redirect('404')

    context = {'pic':picture}
    return render(request,'restaurant/image.html',context)


def about(request):
    data = About.objects.all()[0]
    context = {'data': data}
    return render(request, 'restaurant/about.html', context)


def page_not_found(request):
    return render(request,'restaurant/404.html')



