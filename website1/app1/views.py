from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Contact
from .models import Register
from .models import Product
from .models import Cart
from .models import Order




# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({},request))

def about(request):
    template = loader.get_template("about.html")
    return HttpResponse(template.render({},request))

def contact(request):
    if request.method == 'POST':
        cname =request.POST["name"]
        cemail =request.POST["email"]
        cmsg = request.POST["text"]

        con =Contact(
            con_name = cname,
            con_email = cemail,
            con_message = cmsg,
        )

        con.save()
    template = loader.get_template("contact.html")
    return HttpResponse(template.render({},request))

def register(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect("/account")
    if request.method == 'POST':
        rname =request.POST["name"]
        remail =request.POST["email"]
        rmobile = request.POST["mobile"]
        ruser = request.POST["username"]
        rpswd = request.POST["pswd"]
        exist = Register.objects.filter(reg_username = ruser)
        if exist:
            return HttpResponseRedirect("/register")
        else:
            con =Register(
                reg_name = rname,
                reg_email = remail,
                reg_mobile = rmobile,
                reg_username = ruser,
                reg_password = rpswd,
            )
            con.save()

    template = loader.get_template("register.html")
    return HttpResponse(template.render({},request))

def login(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect("/account")
    if request.method == 'POST':
        loguser=request.POST["username"]
        logpswd=request.POST["pswd"]
        login = Register(reg_username = loguser,reg_password = logpswd)
        if login:
            request.session['usersession'] = loguser
            return HttpResponseRedirect("/account")
        
    template = loader.get_template("login.html")
    return HttpResponse(template.render({},request))

def account(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect("/login")
    template = loader.get_template("accountpage.html")
    return HttpResponse(template.render({},request))

    
def logout(request):
    if 'usersession' in request.session:
        del request.session['usersession']
    return HttpResponseRedirect("/login")

def addproduct(request):
    if request.method =='POST':
        pname = request.POST['productname']
        pprice = request.POST['price']
        pimage =request.FILES['image']

        product = Product(
            pro_name = pname,
            pro_price = pprice, 
            pro_image = pimage,

        )
        product.save()

    template = loader.get_template("addproduct.html")
    return HttpResponse(template.render({},request))

def product(request):
    products=Product.objects.all().values

    context={
        'product' : products
    }
    template = loader.get_template("product.html")
    return HttpResponse(template.render(context,request))

def addtocart(request,id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect("/login")
    
    exist = Cart.objects.filter(cart_proid=id,cart_user=request.session["usersession"])
    if exist:
        exstcart = Cart.objects.filter(cart_proid=id,cart_user=request.session["usersession"])[0]
        exstcart.cart_qty+=1
        exstcart.cart_amount= exstcart.cart_qty * exstcart.cart_price
        exstcart.save()
    else:

        pro = Product.objects.filter(id=id)[0]

        cart = Cart(cart_user = request.session["usersession"],
                    cart_proid=pro.id,
                    cart_name=pro.pro_name,
                    cart_price=pro.pro_price,
                    cart_image=pro.pro_image,
                    cart_qty=1,
                    cart_amount=pro.pro_price)
        cart.save()
    return HttpResponseRedirect("/cart")

def cart(request):
   if 'usersession' not in request.session:
    return HttpResponseRedirect('/login')
   #delete cart item
   if 'del' in request.GET:
       id = request.GET['del']
       delcart = Cart.objects.filter(id=id)[0]
       delcart.delete()

    #change cart quantity
   if 'q' in request.GET:
       q = request.GET['q']
       cp = request.GET['cp']
       cart3=Cart.objects.filter(id=cp)[0]

       if q=='inc':
           cart3.cart_qty+=1
       elif q=='dec':
           if(cart3.cart_qty>1):
               cart3.cart_qty-=1
       cart3.cart_amount=cart3.cart_qty * cart3.cart_price
       cart3.save()
       
   user = request.session["usersession"]
   cart=Cart.objects.filter(cart_user=user).values()
   cart2=Cart.objects.filter(cart_user=user)

   tot = 0
   for x in cart2:
       tot+=x.cart_amount

   shp = tot * 10/100
   gst = tot * 18/100

   gtot = tot+shp+gst

   request.session["tot"] = tot
   request.session["gst"] = gst
   request.session["shp"] = shp
   request.session["gtot"] = gtot

   context={
       'cart':cart,
       'tot':tot,
       'gst':gst,
       'shp':shp,
       'gtot':gtot
   }

   template = loader.get_template("cart.html")
   return HttpResponse(template.render(context,request))

def checkout(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    co = 0
    adrs = dtype = ""

    #After order submit

    if 'dlv_adrs' in request.POST:
        adrs = request.POST["dlv_adrs"]
        dtype = request.POST["dlv_type"]
        co = 1

    user = request.session["usersession"]

    #delete old data from orders
    oldodr=Order.objects.filter(order_user=user,order_status=0)
    oldodr.delete()

    #add cart data to order table
    cart=Cart.objects.filter(cart_user=user)
    for x in cart:
        odr = Order(order_user = x.cart_user,
                    order_name = x.cart_name,
                    order_price = x.cart_price,
                    order_image = x.cart_image,
                    order_qty = x.cart_qty,
                    order_amount = x.cart_amount,
                    order_address = adrs,
                    order_dlvtype = dtype,
                    order_status =0
                )
        odr.save()
        #  display order data

    order =Order.objects.filter(order_user=user,order_status=0).values()

    tot = request.session["tot"]
    gst = request.session["gst"]
    shp = request.session["shp"]
    gtot = request.session["gtot"]

    context={
        'order':order,
        'tot':tot,
        'gst':gst,
        'shp':shp,
        'gtot':gtot,
        'co':co
    }
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))

def confirmorder(request):
     if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
     user =request.session["usersession"]
     order=Order.objects.filter(order_user=user,order_status=0)
     for x in order:
         x.order_status=1
         x.save()
     template = loader.get_template("confirmorder.html")
     return HttpResponse(template.render({},request))

def myorders(request):
    user =request.session["usersession"]
    order=Order.objects.filter(order_user=user,order_status=1)
    context = {
        'order':order
    }
    template = loader.get_template("myorders.html")
    return HttpResponse(template.render(context,request))







       
   
