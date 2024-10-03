from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('',views.index,name='index'),
        path('about',views.about,name='about'),
        path('contact',views.contact,name='contact'),
        path('register',views.register,name='register'),
        path('login',views.login,name='login'),
        path('account',views.account,name='account'),
        path('logout',views.logout,name='logout'),
        path('addproduct',views.addproduct,name='addproduct'),
        path('product',views.product,name='product'),
        path('addtocart/<int:id>',views.addtocart,name='addtocart'),
        path('cart',views.cart,name='cart'),
        path('checkout',views.checkout,name='checkout'),
        path('confirmorder',views.confirmorder,name='confirmorder'),
        path('myorders',views.myorders,name='myorders')


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)