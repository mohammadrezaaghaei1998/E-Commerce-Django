from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from . import views
from django.contrib.auth import views as auth_views


from rest_framework.routers import DefaultRouter
from store.api_views import ProductViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path("",views.HOME,name="home"),
    path("base/",views.BASE,name="base"),
    path("subscribe/",views.SUBSCRİBE,name="subscribe"),
    path("about/",views.ABOUT,name="about"),
    path("products/",views.PRODUCTS,name="products"),
    path("contact/",views.CONTACT,name="contact"),
    path("search/",views.SEARCH,name="search"),
    path("<str:id>",views.DETAIL,name="detail"),
    path("login/",views.LOGIN,name="login"),
    path("register/",views.REGISTER,name="register"),
    path('logout/', views.LOGOUT, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.ORDER_SUCCESS, name='order_success'),
    path('payment/', views.payment, name='payment'),

    
    #CART OPTİONS
    path('add/<int:id>/', views.cart_add, name='cart_add'),
    path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart_detail/',views.cart_detail,name='cart_detail'),

    #DASHBOARD
    path('dashboard/',views.DASHBOARD,name='dashboard'),
    path('favorite/<int:id>/', views.add_to_favorite, name='add_to_favorite'),
    path('favorite/remove/<int:id>/', views.remove_from_favorite, name='remove_from_favorite'),
    path('favorite/', views.favorite_list, name='favorite_list'),
    path('product/<int:id>/', views.favorite_detail, name='product_detail'),
    path('get_favorite_count/', views.get_favorite_count, name='get_favorite_count'),

    #PASSWORD
    path('reset_password/', auth_views.PasswordResetView.as_view
         (template_name='main/reset_password.html')
         ,name='reset_password'),
    path('reset-password_sent/', auth_views.PasswordResetDoneView.as_view
         (template_name='main/password_reset_sent.html')
         ,name='reset-password_done'),
    path('reset-password_complete/', auth_views.PasswordResetCompleteView.as_view
         ()
         ,name='password_reset_complete'),
    path('reset/uidb64/<token>', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),



    #Api 
    path('api/', include(router.urls)),

]

urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)