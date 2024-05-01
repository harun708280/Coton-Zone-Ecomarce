from django.urls import path
from.import views
from.form import LoginForm
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('shop/',views.shop,name='shop'),
    path('product_details/<int:pk>/', views.ProductdetailsView.as_view(), name='product_details'),
    path('checkout/',views.checkout,name='checkout'),
    path('blog/',views.blog,name='blog'),
    path('blog_details/',views.blog_details,name='blog-details'),
    path('cart/',views.show_cart,name='cart'),
    path('add-to-cart',views.cart,name='add-to-cart'),
    path('delete-cart/<int:id>',views.delete_cart,name='delete_cart'),
    path('delete_order/<int:id>',views.Delete,name='delete_order'),
    path('contract/',views.contract,name='contract'),
    path('registration/',views.registration,name='registration'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    path('plus_cart',views.plus_cart,name="plus_cart"),
    path('minas_cart',views.minas_cart,name="minas_cart"),
    path('plus_cart',views.plus_cart,name="plus_cart"),
    path('minas_cart',views.minas_cart,name="minas_cart"),
    path('man/',views.man,name='man'),
    path('women/',views.women,name='women'),
    path('error/',views.carterror,name='eror'),
    path('discaunt/',views.discaunt,name='discaunt'),
    path('kids/',views.kids,name='kids'),
    path('Accessories/',views.Accessories,name='Accessories'),
    path('Cos/',views.Cosmetics,name='Cos'),
    path('checkout/',views.checkout,name='checkout'),
    path('order/',views.Orderplaceds,name='order'),
    path('orderss/',views.orderss,name='ord'),
    path('wishlist/',views.Show_wishlist,name='wishlist'),
    path('wc/',views.wishlist,name='wc'),
    path('wish_del/<int:id>',views.wishs_Delate,name='wish_dele'),
    path('search/',views.Search,name='search'),
    path('subscribe/',views.subscribes,name='sb')
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
