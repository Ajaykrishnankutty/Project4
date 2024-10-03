from django.contrib import admin
from .models import Contact
from .models import Register
from .models import Product
from .models import Cart,Order

# Register your models here.

admin.site.register(Contact)
admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)


