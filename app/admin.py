from django.contrib import admin
from .models import*


class Product_Images(admin.TabularInline):
    model = Product_Image


class Additional_Informations(admin.TabularInline):
    model = Additional_Information    



class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images,Additional_Informations)
    list_display = ('product_name','price','category','section')
    list_editable= ('category','section')



class Doctor_Admin(admin.ModelAdmin):
    list_display = ('name','speciality','experience','degree','fees')
    list_editable= ('speciality','fees')

class Booking_Admin(admin.ModelAdmin):
    list_display = ('user','doctor_name','time','date','contact_type','contact_number','payment_type')
    # list_editable= ('speciality','fees')


admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Doctor,Doctor_Admin)
admin.site.register(booking,Booking_Admin)