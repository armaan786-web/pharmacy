from urllib import request
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.


class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Category(models.Model):
    main_Category = models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        # return self.name
        return self.name + " -- " + self.main_Category.name


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

       

class Product(models.Model):
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    featured_image = models.CharField(max_length=500)    
    product_name = models.CharField(max_length=50)
    # prod_img = models.ImageField(upload_to="media/Prod_img")
    price = models.PositiveIntegerField()
    Discount = models.IntegerField()
    tax = models.IntegerField(default = 0, null=True)
    packing_cost = models.IntegerField(default = 0,null=True)
    Product_information = RichTextField()
    brand_Name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Tags = models.CharField(max_length=100)
    Description = RichTextField()
    section = models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='',max_length=500,null=True,blank=True)


    def __str__(self):
        return self.product_name + " -- " + self.category.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_details", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)








class Product_Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Image_Url = models.ImageField(upload_to = 'product_pic')
    
    # Image_Url = models.CharField(max_length=200) 



class Additional_Information(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detial = models.CharField(max_length=100)
    
class Doctor(models.Model):
    profile_pic = models.ImageField(upload_to = 'doctor/profile_pic')
    name = models.CharField(max_length=50)
    speciality = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    degree = models.CharField(max_length=50)
    fees = models.IntegerField()

    def __str__(self):
        return self.name
  

    
class booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
   
    time = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    contact_type = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    

  

