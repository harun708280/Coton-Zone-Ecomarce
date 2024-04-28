from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .form import RegestrationForm
from django.contrib import messages
from.models import *
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.
def home(request):
    pro=Product.objects.all()[:8]
    pt=Cetagory.objects.all()
    bs=Best_sels.objects.all()[:4]
    ht=hottrend.objects.all()[:4]
    f=feature.objects.all()[:4]
    ct=Cetagory.objects.get(name='Man')
    pf=Product.objects.filter(cetagory=ct)
    ma=banner.objects.filter(name='Men’s Fashion')
    acc=banner.objects.filter(name='Accessories')
    w=banner.objects.filter(name='Women’s Fashion')
    kids=banner.objects.filter(name='Kid’s Fashion')
    cos=banner.objects.filter(name='Cosmetics')
    
    
    
    return render(request,'index.html',{'p':pro,'pt':pt,'bs':bs,'ht':ht,'f':f,'pf':pf,'m':ma,'a':acc,'w':w,'k':kids,'c':cos})
class ProductdetailsView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            pd=Product.objects.get(pk=pk)
            related_product=Product.objects.filter(cetagory=pd.cetagory).exclude(pk=pk)
            quantity=1
            
            try:
                cart=Cart.objects.get(Q(product=pd)& Q(user=request.user))
                quantity=cart.quantity
            
            except Cart.DoesNotExist:
                quantity=1
            return render(request,'product-details.html',{'pd':pd,'r':related_product,'quantity':quantity})
        
        else:
            return redirect('login')

def cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product_quantity = int(request.GET.get('product_quantity', 1))  # Default quantity to 1 if not provided
    product = Product.objects.get(id=product_id)
    
    try:
        cart_item = Cart.objects.get(user=user, product=product)
        cart_item.quantity = product_quantity
        cart_item.save()
    except Cart.DoesNotExist:
        # Create a new cart item if it doesn't exist
        cart_item = Cart(user=user, product=product, quantity=product_quantity)
        cart_item.save()

    return redirect('/cart')


def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tamount=(p.quantity*p.product.price)
                amount=amount+tamount
                vat=amount+10
            return render(request,'shop-cart.html',{'totalamount':amount,'cart':cart,'line_total':Cart.line_total,'vat':vat})
        else:
            return redirect('eror')       
def delete_cart(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect('/cart')
            
def shop(request):
    p=Product.objects.all()[3:]
    return render(request,'shop.html',locals())



def checkout(request):
    return render(request,'checkout.html')

def blog_details(request):
    return render(request,'blog-details.html')

def blog(request):
    return render(request,'blog.html')

def contract(request):
    return render(request,'contact.html')

def login(request):
    return render(request,'login.html')

def registration(request):
    form=RegestrationForm()
    if request.method == 'POST':
        form = RegestrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            
        else:
            return render(request,'er.html')
    return render(request,'regestration.html')
def plus_cart(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        cart = Cart.objects.get(Q(id=cart_id) & Q(user=request.user))
        cart.quantity += 1
        cart.save()
        line_total = cart.quantity * cart.product.price
        carts = Cart.objects.filter(user=request.user)
        cart_total = 0
        for i in carts: 
            cart_total = cart_total + i.line_total()

        print(cart_total)
        return JsonResponse({"status":"success", "quantity": cart.quantity,"line_total":line_total,"cart_total":cart_total})

def minas_cart(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        cart = Cart.objects.get(Q(id=cart_id) & Q(user=request.user))
        if cart.quantity <= 1:
            cart.quantity = 1
        else:
            cart.quantity -= 1
        cart.save()
        line_total = cart.quantity * cart.product.price
        carts = Cart.objects.filter(user=request.user)
        cart_total = 0
        for i in carts:
            cart_total = cart_total + i.line_total()
      
        return JsonResponse({"status":"success", "quantity": cart.quantity,"line_total":line_total,"cart_total":cart_total})

def man(request):
    ct=Cetagory.objects.get(name='Man')
    
    p = Product.objects.filter(cetagory=ct)  
    pa=Product.objects.filter(name='T-Shirt')
    return render(request, 'man.html', {'p': p,'pa':pa})


def women(request):
    ct=Cetagory.objects.get(name='Women')
    p=Product.objects.filter(cetagory=ct)
    return render(request,'women.html',{'p':p})

def carterror(request):
    return render(request,'carteroro.html')

def discaunt(request):
    po=Cetagory.objects.get(name='Discaunt')
    p=Product.objects.filter(cetagory=po)
    return render(request,'discaunt.html',{'p':p})

def kids(request):
    pc=Cetagory.objects.get(name='Kid’s fashion')
    p=Product.objects.filter(cetagory=pc)
    return render(request,'kids.html',locals())

def Accessories(request):
    pc=Cetagory.objects.get(name='Accessories')
    p=Product.objects.filter(cetagory=pc)
    return render(request,'accessoris.html',locals())

def Cosmetics(request):
    pc=Cetagory.objects.get(name='Cosmetics')
    p=Product.objects.filter(cetagory=pc)
    return render(request,'Cosmetics.html',locals())