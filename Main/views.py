from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .form import *
from django.contrib import messages
from.models import *
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.
from django import template
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest


register = template.Library()


def home(request):
    total_cart=0
    total_wish=0
    if request.user.is_authenticated:
        #subscribe=request.POST.get('subscribe')
        total_cart=len(Cart.objects.filter(user=request.user))
        total_wish=len(Wishlist.objects.filter(user=request.user))
    
    user=request.user
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
    #sub=Subscribe(user=user,email=subscribe)
    
    #sub.save()
    #messages.success(request,'Congratulation SuccesFully Your Subcribtion')
    
    
    return render(request,'index.html',{'p':pro,'pt':pt,'bs':bs,'ht':ht,'f':f,'pf':pf,'m':ma,'a':acc,'w':w,'k':kids,'c':cos,'total_cart':total_cart,'total_wish':total_wish})
class ProductdetailsView(View):
    def get(self,request,pk):
        total_cart=0
        total_wish=0
        if request.user.is_authenticated:
            total_cart=len(Cart.objects.filter(user=request.user))
            total_wish=len(Wishlist.objects.filter(user=request.user))
            pd=Product.objects.get(pk=pk)
            reviews=Review.objects.filter(product=pd)
            comment_form=Review_From()
            related_product=Product.objects.filter(cetagory=pd.cetagory).exclude(pk=pk)
            quantity=1
            
            try:
                cart=Cart.objects.get(Q(product=pd)& Q(user=request.user))
                quantity=cart.quantity
            
            except Cart.DoesNotExist:
                quantity=1
            return render(request,'product-details.html',{'pd':pd,'rr':related_product,'quantity':quantity,'r':reviews,'cf':comment_form,'total_cart':total_cart,'total_wish':total_wish})
        
        else:
            return redirect('login')
    
    def post(self,request,pk):
        product=Product.objects.get(pk=pk)
        comment_form=Review_From(request.POST)
        
        if comment_form.is_valid():
            new_review=comment_form.save(commit=False)
            new_review.product=product
            new_review.user=request.user
            new_review.save()
            return redirect('product_details',pk=pk)
        
        else:
            return redirect('home')

def cart(request):
    
    user = request.user
    product_id = request.GET.get('prod_id')
    
    # Check if the product_id is provided and not empty
    if not product_id:
        return HttpResponseBadRequest("Product ID is required.")
    
    try:
        product = Product.objects.get(id=product_id)
        product_quantity = int(request.GET.get('product_quantity', 1))  # Default quantity to 1 if not provided
        
        try:
            cart_item = Cart.objects.get(user=user, product=product)
            cart_item.quantity = product_quantity
            cart_item.save()
        except Cart.DoesNotExist:
            # Create a new cart item if it doesn't exist
            cart_item = Cart(user=user, product=product, quantity=product_quantity)
            cart_item.save()

        return redirect('/cart')
    except Product.DoesNotExist:
        return HttpResponseBadRequest("Invalid product ID.")


def show_cart(request):
    total_cart=0
    total_wish=0
    
    if request.user.is_authenticated:
        total_cart=len(Cart.objects.filter(user=request.user))
        
        total_wish=len(Wishlist.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        vat = 0.0
        
        cart_products = Cart.objects.filter(user=user)
        if cart_products:
            for cart_item in cart_products:
                tamount = cart_item.quantity * cart_item.product.price
                amount += tamount
                vat = amount + 10

            if request.method == 'POST':
                cuponform = CuponcodeForm(request.POST)
                if cuponform.is_valid():
                    current_time = timezone.now()
                    code = cuponform.cleaned_data.get('code')
                    
                    current_coupon = Cupon.objects.get(code=code)
                    if current_coupon.valid_to >= current_time.date() and current_coupon.active:
                            discount_price = (current_coupon.discaunt / 100) * amount
                            coupon_discount = amount - discount_price
                            request.session['total_discount'] = coupon_discount 
                            request.session['coupon_code'] = code
                            print(coupon_discount)
                            return redirect('cart')
                        
                    else:
                        return redirect('home')
                   
            coupon_discount = request.session.get('total_discount')
            coupon_code = request.session.get('coupon_code')
            return render(request, 'shop-cart.html', {'totalamount': amount, 'cart': cart, 'line_total': Cart.line_total, 'vat': vat, 'coupon_discount': coupon_discount, 'code': coupon_code,'total_cart':total_cart,'total_wish':total_wish})
        
        
    
    return render(request,'carteroro.html')      
def delete_cart(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect('/cart')
def Delete(request,id):
    order=OrderPlaced.objects.get(id=id)
    order.delete() 
    return redirect('ord')        
def shop(request):
    total_cart=0 
    total_wish=0
    if request.user.is_authenticated:
        
        total_cart=len(Cart.objects.filter(user=request.user))
        total_wish=len(Wishlist.objects.filter(user=request.user))
    p = Product.objects.all()
    paginator = Paginator(p, 9)
    page_number = request.GET.get('page')
    
    print("Page Number:", page_number) 
    
    datafinal = paginator.get_page(page_number)
    return render(request, 'shop.html', {'p':datafinal,'total_cart':total_cart,'total_wish':total_wish})




def checkout(request):
    return render(request,'checkout.html')

def blog_details(request):
    return render(request,'blog-details.html')

def blog(request):
    return render(request,'blog.html')

def contract(request):
    if request.user.is_authenticated:
        names = request.POST.get('names')  # corrected field name
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        user = request.user
        data={
            'name':names,
            'email':email,
            'message':comment
        }
        email_message = '''
        From : {}
        Name : {}
        Comment : {}
        '''.format(data['email'],data['name'],data['message'])
        send_mail('New Message Revidve CottonZon Contract',email_message,'',['harun708280@gmail.com'])
        en = SMS(user=user, mnb=names, mkl=email, cmm=comment)
        en.save()
        messages.success(request, 'SMS Send Done')
        return render(request, 'contact.html')
    else:
        return redirect('login')


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

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        amount = sum(cart_item.quantity * cart_item.product.price for cart_item in cart_items)

        if request.method == 'POST':
            coupon_form = CuponcodeForm(request.POST)
            if coupon_form.is_valid():
                code = coupon_form.cleaned_data.get('code')
                try:
                    coupon = Cupon.objects.get(code=code)
                    if coupon.is_valid():
                        discount_amount = (coupon.discount / 100) * amount
                        total_amount = amount - discount_amount
                        request.session['coupon_code'] = code
                        request.session['total_discount'] = discount_amount
                        return redirect('cart')
                    else:
                        
                        return redirect('checkout')
                except Cupon.DoesNotExist:
                   
                    return redirect('checkout')

        coupon_code = request.session.get('coupon_code')
        total_discount = request.session.get('total_discount', 0)
        return render(request, 'checkout.html', {'cart': cart_items, 'totalamount': amount, 'coupon_code': coupon_code, 'total_discount': total_discount})

    return render(request, 'login.html')
   
def Orderplaceds(request):
    
    if request.method == 'POST':
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        country=request.POST.get('country')
        address1=request.POST.get('address1')
        address2=request.POST.get('address2')
        city=request.POST.get('city')
        zip=request.POST.get('zip')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        #payment=request.POST.get('payment')
        
    
    
    user=request.user
    cart=Cart.objects.filter(user=user)
    for c in cart :
        OrderPlaced(user=user,first_name=first_name,last_name=last_name,country=country, address1= address1,address2=address2, city= city,zip=zip,phone=phone,email=email,product=c.product,quantity=c.quantity).save()
        c.delete()
        
    return redirect('ord')    
    
    
def orderss(request):
    amount = 0.0
    orders = OrderPlaced.objects.filter(user=request.user)
    total_price = sum(order.quantity * order.product.price for order in orders)
    
    if request.method == 'POST':
        coupon_form = CuponcodeForm(request.POST)
        if coupon_form.is_valid():
            code = coupon_form.cleaned_data.get('code')
            try:
                coupon = Cupon.objects.get(code=code)
                if coupon.is_valid():
                    discount_amount = (coupon.discount / 100) * total_price
                    total_amount = total_price - discount_amount
                    request.session['coupon_code'] = code
                    request.session['total_discount'] = discount_amount
                    return redirect('cart')
                else:
                    return redirect('checkout')
            except Cupon.DoesNotExist:
                return redirect('checkout')
        
    coupon_code = request.session.get('coupon_code')
    total_discount = request.session.get('total_discount', 0)
    
    return render(request, 'order.html', {'orders': orders, 'total_discount': total_discount, 'total_price': total_price})

    
from django import template

register = template.Library()

def Show_wishlist(request):
    wishlists=Wishlist.objects.filter(user=request.user)
    if wishlists:
     return render(request,'wishlist.html',{'w':wishlists})
    
    else:
        return render(request,'carteroro.html')
 
 
 
 
 

def wishlist(request,):
    if request.user.is_authenticated:
        user=request.user
        product_id=request.GET.get('prod_id')
        product=Product.objects.get(id=product_id)
        if product:
            try:
                wish_item=Wishlist.objects.get(user=user,product=product)
                
                wish_item.save()
            
            except Wishlist.DoesNotExist:
                wish_item=Wishlist(user=user,product=product)
                wish_item.save()
            return redirect('home')
        
        else:
    
         return render(request,'carteroro.html')

def wishs_Delate(request,id):
    wish=Wishlist.objects.get(id=id)
    wish.delete()
    return redirect('wishlist')
    
    
def Search(request):
    if request.method == 'GET':
        search=request.GET.get('search')
        if search:
            product=Product.objects.filter(name__icontains=search)
            return render(request,'search.html',{"product":product})
        
        else:
            return render(request,'search.html')
   
def subscribes(request):
    if request.user.is_authenticated:
        subscribe=request.POST.get('subscribe')
    user=request.user
    
    subs=Subscribe(user=user,email=subscribe)
    subs.save()
    messages.success(request,'Congratulation For Your Subscriotion')
    return redirect('home')