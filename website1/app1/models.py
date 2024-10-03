from django.db import models

# Create your models here.

class Contact(models.Model):
    con_name = models.CharField(max_length=255)
    con_email = models.EmailField(max_length=255)
    con_message = models.TextField()

    def __str__(self):
        return self.con_name

class Register(models.Model):
    reg_name = models.CharField(max_length=255)
    reg_email = models.EmailField(max_length=255)
    reg_mobile = models.IntegerField()
    reg_username = models.CharField(max_length=255)
    reg_password = models.CharField(max_length=255)

    def __str__(self):
        return self.reg_name
    
class Product(models.Model):
    pro_name = models.CharField(max_length=2555)
    pro_price = models.FloatField()
    pro_image =models.FileField(null=True,upload_to="products")

    def __str__(self):
        return self.pro_name
    
class Cart(models.Model):
    cart_user = models.CharField(max_length=250,default=None)
    cart_proid = models.IntegerField(null=True)
    cart_name = models.CharField(max_length=250)
    cart_price = models.FloatField(max_length=250)
    cart_image = models.FileField(null=True)
    cart_qty = models.IntegerField()
    cart_amount = models.FloatField()

    def __str__(self):
        return self.cart_name
    
class Order(models.Model):
        order_user = models.CharField(max_length=250,default=None)
        order_name = models.CharField(max_length=250)
        order_price = models.CharField(max_length=250)
        order_image = models.CharField(null=True,max_length=250)
        order_qty = models.IntegerField()
        order_amount = models.IntegerField()
        order_address = models.TextField(null=True)
        order_dlvtype = models.CharField(null=True,max_length=10)
        order_status = models.IntegerField(default=0)

        def __str__(self):
            return self.order_name




