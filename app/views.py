from email import message
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.db.models import Max,Min,Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Create your views here.

def BASE(request):
    return render(request,'base.html')

def BASE2(request):
    return render(request,'includes/shop/base.html')

def home(request):
    main_category = Main_Category.objects.all().order_by('-id')[:6]
    category_after_four = Main_Category.objects.all().order_by('-id')[6:]
    main_Cat = Main_Category.objects.all()[:5]
    sub_cat = Category.objects.all()
    product = Product.objects.all()
    prod = Product.objects.filter(section__name="Featured Products")
    trending = Product.objects.filter(section__name="Trending Products")
    categoryID = request.GET.get('category')
    

    context = {
        'main_category':main_category,
        'main_Cat': main_Cat,
        'category_after_four':category_after_four,
        'sub_cat':sub_cat,
        'prod':prod,
        'product':product,
        'trending':trending
        
    }
    return render(request,'Main/home_nw.html',context)

def shop(request,id):
    product = Product.objects.filter(category=id)
    if product.exists():
        product = Product.objects.filter(category=id)
    # else:
    #     return redirect('404')
    sub_cat = Category.objects.all()
    # product = Product.objects.all()
    ATOZ = Product.objects.filter(category=id)
    
    
    

    context = {
        'sub_cat':sub_cat,
        'product':product,
        'ATOZ':ATOZ,
        
    }
    # product = Product.objects.all().filter(id=id)
    return render(request,'Main/shop.html',context)



@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    # print("helooooooooooooo",packing_cost,tax)
    context = {
        'packing_cost':packing_cost,
        'tax':tax,

    }
    return render(request, 'cart/cart.html',context)





def checkout(request):
    return render(request,'checkout.html')

def wishlist(request):
    return render(request,'wishlist.html')

def product_details(request,slug):
    product = Product.objects.filter(slug=slug)
    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')

    # img = Product_Image.objects.get(id=id)
    return render(request,'Main/product_details.html',{'product':product})

def MY_ACCOUNT(request):
    return render(request,'account/register.html')

def REGISTER_SAVE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request,"Username is already exists")
            return redirect('my_account')
        
        if User.objects.filter(email = email).exists():
            messages.error(request,"Email Id are already exists")
            return redirect('my_account')

        try:

            user =  User(
                username = username,
                email = email,
                
            )
            user.set_password(password)
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect(reverse("login"))
        except:

            messages.error(request,"Failed to Registration")
            return HttpResponseRedirect(reverse("my_account"))
            
        
    return redirect('my_account')


def LOGIN(request):
    return render(request,'account/login.html')

def DOLOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =  request.POST.get('password')

        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Email and Password are Invalid !!")
            return redirect('login')
    return redirect('login')

@login_required(login_url='/accounts/login/')
def PROFILE(request):
    return render(request,'Main/profile.html')

@login_required(login_url='/accounts/login/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        fname = request.POST.get("ltn__name")
        lname = request.POST.get("ltn__lastname")
        username = request.POST.get("ltn__username")
        email = request.POST.get("ltn__email")
        password = request.POST.get("ltn__password")
        confirm_password = request.POST.get("ltn__confirm_psw")
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = fname
        user.last_name = lname
        user.username = username
        user.email = email

        if password != confirm_password:
            messages.error(request,"Password does not match !!")
            return redirect('profile')
        if password != None and password != "":
            user.set_password(password)
        messages.success(request,"Profile are Successfully Updated !!")
        user.save()
    return redirect('profile')



def list_of_doctor(request):
    doctor = Doctor.objects.all()
    return render(request, "Main/list_of_doctor.html",{'doctor':doctor})



def doctor_booking(request,id):
    doctor = Doctor.objects.get(id = id)
    if request.method == "POST":
        select_tym = request.POST.get('select_tym')
        selected_date = request.POST.get('selected_date')
        contact_type = request.POST.get('contact_type')
        contact_number = request.POST.get('contact_number')
        payment_type = request.POST.get('payment_type')

        print("seleeeeeeee",select_tym)
        
        try:

            idd = request.user.id
        # print("idddddddddd",idd)
        

            # book = booking.objects.get(id = User.id)
            book = booking.objects.create(user_id=idd,doctor_name=doctor,time=select_tym,select_date=selected_date,contact_type=contact_type,contact_number=contact_number,payment_type=payment_type)
            # book.time =select_tym
            # book.save()
            messages.success(request,"Successfully Added Booking")
            return HttpResponseRedirect(reverse("list_of_doctor"))
        except:
            messages.error(request,"Failed to Booking")
            return HttpResponseRedirect(reverse("list_of_doctor"))
            

        # booking.
        # print("bookingggggggggggg",booking)
    return render(request, "Main/doctor_booking.html",{'doctor':doctor})


def Error404(request, exception):
    return render(request,'errors/404.html')