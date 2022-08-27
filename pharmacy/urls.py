
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app import views
from django.views.static import serve 
from django.urls import re_path

admin.site.site_header = "oranju Admin"
admin.site.site_title = "oranju Admin Portal"
admin.site.index_title = "Welcome to oranju Researcher Portal"

urlpatterns = [
     

     re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
     re_path(r'^static/(?P<path>.*)$', serve,{'documen t_root': settings.STATIC_ROOT}),

     path("404",views.Error404,name="404"),
     path('admin/', admin.site.urls),
     path('base/',views.BASE,name="base"),
     path('base2/',views.BASE2,name="base2"),
     # path('',views.home,name="home"),
     path('',views.home,name="home"),
     path('shop/<int:id>',views.shop,name="shop"),
     
     path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
     path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
     path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
     path('cart/item_decrement/<int:id>/',
          views.item_decrement, name='item_decrement'),
     path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
     path('cart/cart-detail/',views.cart_detail,name='cart_detail'),






     path('checkout/',views.checkout,name="checkout"),
     path('wishlist/',views.wishlist,name="wishlist"),
     path('product-details/<slug:slug>',views.product_details,name="product_details"),


    ############## account urls ################

     path('account/my-account/',views.MY_ACCOUNT,name="my_account"),
     path('account/register_Save/',views.REGISTER_SAVE,name="register_save"),
     path('account/login/',views.LOGIN,name="login"),
     path('account/dologin/',views.DOLOGIN,name="dologin"),


     path('accounts/',include('django.contrib.auth.urls')),



    ################## profile urls ######################

     path('account/profile',views.PROFILE,name="profile"),
     path('account/profile/update',views.PROFILE_UPDATE,name="profile_update"),


    ########################### list of doctor #####################

     path("list_of_doctor",views.list_of_doctor,name="list_of_doctor"),
     path("doctor_booking/<int:id>",views.doctor_booking,name="doctor_booking"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

handler404 = 'app.views.Error404'
