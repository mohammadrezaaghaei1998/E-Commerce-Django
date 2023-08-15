from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from store.models import Product,Categories,Filter_price,Color,Brand,Contact_us,Cart,CartItem,UserInfo,Order,Payment,FavoriteProduct,Notification
from store.forms import PaymentForm, UserInfoForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import secrets
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
# from .helpers import send_forget_password_mail
# import uuid
# from django.core.mail import send_mail








# from django.utils import timezone
# from decimal import Decimal




CART_SESSION_ID = 'cart'




def BASE(request):
    return render(request,"main/base.html")



def HOME(request):
    if request.user.is_authenticated:
        cart_item_count = get_cart_item_count(request.user)
    else:
        cart_item_count = 0

    products = Product.objects.filter(status='Publish')
    
    context = {
        'products': products,
        'cart_item_count': cart_item_count,
        
    }

    return render(request, "main/index.html", context)




def get_cart_item_count(user):
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            cart_items = cart.cartitem_set.all()
            return cart_items.count()
        else:
            return 0 
    return 0




def SUBSCRİBE(request):
    return render(request,"main/subscribe.html")



def ABOUT(request):
    return render(request,"main/about.html")



def PRODUCTS(request):
    product = Product.objects.filter(status = 'Publish')
    categories = Categories.objects.all()
    filter_price = Filter_price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()


    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLORID = request.GET.get('color')
    BRANDID = request.GET.get('brand')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')

    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')

    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')


    if CATID:
        product = Product.objects.filter(categories=CATID, status='publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price=PRICE_FILTER_ID, status='publish')
    elif COLORID:
        product = Product.objects.filter(color=COLORID, status='publish')
    elif BRANDID:
        product = Product.objects.filter(brand=BRANDID,status='publish')
    elif ATOZID:
        product = Product.objects.filter(status='publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='publish').order_by('-name')
    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='publish').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='publish').order_by('-price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status='publish',condition='New').order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status='publish',condition='Old').order_by('-id')
    else:
        product = Product.objects.filter(status='Publish').order_by('-id')
    
    products_with_discount = Product.objects.filter(status='Publish', discount_price__isnull=False)


    context = {
        'product' : product,
        'categories' : categories,
        'filter_price' : filter_price,
        'color' : color,
        'brand' : brand,
        'products_with_discount': products_with_discount,

    }
    return render(request,"main/products.html",context)



def CONTACT(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            message=message,
        )

        message = message
        email_from = settings.EMAIL_HOST_USER 
        #try:
        send_mail(message,email_from,['mehmetgokdaq@gmail.com'])
        contact.save()
        return redirect('home')
        #except:
           # return redirect('contact')
    

    return render(request,"main/contact.html")



def SEARCH(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(name__icontains = query)

            context = {
                'product':products
            }
            if len(products) == 0:
                messages.warning(request, 'No matching products found.')
            return render(request,'main/search.html',context)
        else:
            return render(request,'main/products.html',{})




# def DETAIL(request, id):
#     product = Product.objects.get(id=id)
#     context = {
#         'product':product
#     }

#     return render(request,"main/detail.html",context)




def DETAIL(request, id):
    try:
        product = Product.objects.get(id=id)
        context = {
            'product': product
        }
        return render(request, "main/detail.html", context)
    except (Product.DoesNotExist, ValueError):
        return HttpResponse("Invalid product ID")






def LOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "main/login.html")





def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        try:
            existing_user = User.objects.get(username=username)
            messages.error(request, "Username already taken.")
            return redirect("register")
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password)
            userinfo = UserInfo.objects.create(user=user)


            # try:
            #     existing_email = User.objects.get(email=email)
            #     messages.error(request, "Email already registered.")
            #     return redirect("register")
            # except User.DoesNotExist:
            #     customer = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("home")
    
    return render(request,"main/register.html")




def LOGOUT(request):
    logout(request)
    return redirect('home')




@login_required(login_url="/login/")
def cart_add(request, id):
    product = Product.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect("home")




@login_required(login_url="/login/")
def item_clear(request, id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    
    cart_item.delete()

    if cart.cartitem_set.exists():
        messages.success(request, f"{product.name} removed from your cart.")
    else:
        messages.success(request, "Your cart is empty.")
    
    return redirect("cart_detail")



@login_required(login_url="/login/")
def item_increment(request, id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    cart_item.quantity += 1
    cart_item.save()
    
    if item_created:
        messages.success(request, f"{product.name} added to your cart.")
    else:
        messages.success(request, f"1 item added to your cart.")
    
    return redirect("cart_detail")

def item_decrement(request, id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f"1 item removed from your cart.")
    else:
        cart_item.delete()
        messages.success(request, f"{product.name} has been removed from your cart.")
    
    return redirect("cart_detail")




@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart.objects.get(user=request.user)
    cart.cartitem_set.all().delete()

    messages.success(request, "Your cart has been cleared.")
    return redirect("cart_detail")





@login_required(login_url="/login/")
def cart_detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        total_price = sum(item.get_total_item_price() for item in cart_items)
        cart_item_count = get_cart_item_count(request.user)

    if not cart_items:
        messages.info(request, "Your cart is empty.")
        cart_item_count = 0 
        cart_items = 0
   
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_item_count': cart_item_count,

    }

    return render(request, 'main/cart_detail.html', context)





@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    try:
        user_info = UserInfo.objects.get(user=request.user)
        user_form = UserInfoForm(request.POST or None, instance=user_info)
    except UserInfo.DoesNotExist:
        user_info = None
        user_form = UserInfoForm(request.POST or None)

    cart_item_count = get_cart_item_count(request.user)

    if request.method == 'POST':
        if user_info is None:  
            user_form = UserInfoForm(request.POST)
            if user_form.is_valid():
                user_info = user_form.save(commit=False)
                user_info.user = request.user
                user_info.save()

        if user_info:
            order, created = Order.objects.get_or_create(cart=cart, user_info=user_info)
        else:
            order, created = Order.objects.get_or_create(cart=cart)


        request.session['user_info_id'] = user_info.id if user_info else None
        return redirect('payment')
    else:
        user_form = UserInfoForm()

    context = {
        'cart_items': cart.cartitem_set.all(),
        'total_price': sum(item.get_total_item_price() for item in cart.cartitem_set.all()),
        'user_info_form': user_form,
        'cart_item_count': cart_item_count
    }

    return render(request, 'main/checkout.html', context)






@login_required
def payment(request):
    user_info_id = request.session.get('user_info_id')
    if not user_info_id:
        return redirect('checkout')

    user_info = UserInfo.objects.get(id=user_info_id)
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()


    

    payment_form = PaymentForm(request.POST or None)
    cart_item_count = get_cart_item_count(request.user)

    if request.method == 'POST':
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.order = Order.objects.get(user_info=user_info)

            payment.generate_reference_code()
                                                                                                                                                                                                                                                                                              
            payment.save()

                
            cart_items = cart.cartitem_set.all()
            for cart_item in cart_items:
                cart_item.ordered = True
                cart_item.save()
                 
            del request.session['user_info_id']
            request.session['payment_done'] = True  
            return redirect('order_success')
    else:
        payment_form = PaymentForm()
    if not cart_items:
        messages.info(request, "Your cart is empty.")
        cart_item_count = 0 
        cart_items = 0
    context = {
        'user_info': user_info,
        'cart_items': cart.cartitem_set.all(),
        'total_price': sum(item.get_total_item_price() for item in cart.cartitem_set.all()),
        'payment_form': payment_form,
        'cart_item_count': cart_item_count,
        
    }
    return render(request, 'main/payment.html', context)





def ORDER_SUCCESS(request):
    return render(request, 'main/order_success.html')







@login_required(login_url="/login/")
def add_to_favorite(request, id):
    product = Product.objects.get(id=id)
    favorite_product, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)
   
    if created:
        messages.success(request, f"{product.name} added to your favorite list.")

        if product.discount_price is not None and product.discount_price < product.price:
            message = f"{product.name} is now on discount!"
            Notification.objects.create(user=request.user, message=message)
    else:
        messages.info(request, f"{product.name} is already in your favorite list.")

    return redirect("products")





@login_required(login_url="/login/")
def favorite_detail(request, id):
    try:
        product = Product.objects.get(id=id)
        favorite_count = get_favorite_count(request.user)
        context = {
            'product': product,
            'favorite_count': favorite_count,  # Pass the favorite count to the template
        }
        if request.method == 'POST':
            favorite_product, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)
            if created:
                messages.success(request, f"{product.name} added to your favorite list.")
            else:
                messages.info(request, f"{product.name} is already in your favorite list.")

        return render(request, "main/favorite_detail.html", context)
    except (Product.DoesNotExist, ValueError):
        return HttpResponse("Invalid product ID")

        

    
@login_required(login_url="/login/")
def remove_from_favorite(request, id):
    product = Product.objects.get(id=id)
    favorite_product = get_object_or_404(FavoriteProduct, user=request.user, product=product)
    favorite_product.delete()

    messages.success(request, f"{product.name} removed from your favorite list.")
    return redirect("dashboard")




@login_required(login_url="/login/")
def favorite_list(request):
    favorite_products = FavoriteProduct.objects.filter(user=request.user)
    favorite_count = favorite_products.count()

    context = {
        'favorite_products': favorite_products,
        'favorite_count': favorite_count,
    }

    return render(request, "main/favorite_list.html", context)




@login_required(login_url="/login/")
def get_favorite_count(user):
    favorite_count = FavoriteProduct.objects.filter(user=user).count()
    print(favorite_count)

    return favorite_count
    





def DASHBOARD(request):
    user = request.user
    notifications = Notification.objects.filter(user=user)
    notifications.update(is_read=True)

    favorite_products = FavoriteProduct.objects.filter(user=user)
    try:
        user_info = user.userinfo
        previous_orders = Order.objects.all()
    except UserInfo.DoesNotExist:
        user_info = None
        previous_orders = None

    previous_orders = Order.objects.filter(user_info=user_info)
    for order in previous_orders:
        order.created_at = timezone.localtime(order.created_at)

    context = {
        'user': user,
        'notifications': notifications,
        'favorite_products': favorite_products,
        'previous_orders': previous_orders,
        
    }

    return render(request, 'main/dashboard.html', context)




# def RESET_PASSWORD(request,token):
#     context ={}
#     try:
#         user_info = UserInfo.objects.get(forget_password_token = token)
#         print(user_info)

#     except Exception as e:
#         print(e)


#     return render(request,'main/reset_password.html')




# def FORGET_PASSWORD(request):
#     try:
#         if request.method == "POST":
#             username = request.POST.get('username')

#             if not User.objects.filter(username=username).first():
#                 messages.success(request,'User Not Found.')
#                 return redirect('forget_password')

          
#             user_obj = User.objects.get(username=username)
#             token = str(uuid.uuid4())
#             send_forget_password_mail(user_obj , token)
#             messages.error(request,'An email sent to your email address.')
#             return redirect('home')

#     except Exception as e:
#         print(e)
#     return render(request,'main/forget_password.html')







