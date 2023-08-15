from django.contrib import admin
from .models import * 
from .forms import PaymentForm



class ImagesTublerinline(admin.TabularInline):
    model = Images

class TagTublerinline(admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline,TagTublerinline]




admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_price)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images)
admin.site.register(Tag)
admin.site.register(FavoriteProduct)




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = []



@admin.register(Contact_us)
class Contact_usAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','message')




@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')




@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ('cart', 'product','quantity')



@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'state', 'street', 'zipcode', 'email', 'phone_number','cart_item')
    

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
   exclude = []
