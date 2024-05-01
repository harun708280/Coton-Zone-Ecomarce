from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class Customer_Contract_From(models.Model):
    name=models.CharField( max_length=50)
    email=models.EmailField( max_length=254)
    message=models.TextField()
    
    def __str__(self):
        return self.name
    
class Cetagory(models.Model):
    
    name=models.CharField( max_length=50,blank=False,null=False)
    image=models.ImageField( upload_to='cetagory', blank=True ,null=True)
    parent=models.ForeignKey('self',  on_delete=models.CASCADE,blank=True, null=True)
    created=models.DateTimeField(  auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
       
        verbose_name_plural='Cetagories'
PRODUCT_SIZE= (
        ('XXL','XXL'),
        ('XL','XL'),
        ('L','L'),
        ('ML','ML')   
    )
class Product(models.Model):
    
    name=models.CharField( max_length=550,blank=False ,null=False)
    
    cetagory=models.ForeignKey(Cetagory, on_delete=models.CASCADE ,blank=False ,null= False)
    
    preview_des=models.CharField( max_length=300,verbose_name='Short Description')
    description=models.TextField(max_length=1000,verbose_name='Description')
    images1=models.ImageField( upload_to='img',)
    iamges2=models.ImageField( upload_to='img2', )
    price=models.FloatField()
    old_price=models.FloatField(default=0.00,blank=True,null=True)
    product_size=models.CharField(choices=PRODUCT_SIZE, max_length=50)
    is_stock=models.BooleanField(default=True)
    date=models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username}"
    
    def line_total(self):
        return self.product.price*self.quantity
    
class hottrend(models.Model):
    name=models.ForeignKey(Product ,verbose_name=("Add Hot Trend Product"), on_delete=models.CASCADE,blank=True,null=True)
    date=models.DateField( auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
       
        verbose_name_plural='Hot Trend'
    
class Best_sels(models.Model):   
    name=models.ForeignKey(Product, verbose_name=("Add to Best Sels Product"), on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
    
    class Meta:
        verbose_name_plural='Best Sels'
    
    
class feature(models.Model):
    name=models.ForeignKey(Product, verbose_name=("Add To Feature Product"), on_delete=models.CASCADE)
    
    date=models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name_plural='Product Feature'
    
    
class banner(models.Model):
    women=models.ImageField(upload_to=None,verbose_name='Women Bennar Change',blank=True,null=True)
    man=models.ImageField(upload_to=None,verbose_name='Man Bennar Change',blank=True,null=True)
    kid=models.ImageField( upload_to=None,verbose_name='Kid’s fashion Benner Change' ,blank=True,null=True)
    cos=models.ImageField( upload_to=None, verbose_name='Cosmetics Benner Change',blank=True,null=True)
    acc=models.ImageField( upload_to=None, verbose_name='Accessories Benner Change',blank=True,null=True)
    name=models.CharField( max_length=50,verbose_name='Product Cetagory Name',blank=False,null=False)
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    product=models.ForeignKey(Product, verbose_name=('See Rating Product'), on_delete=models.CASCADE)
    user=models.ForeignKey(User, verbose_name=('User Name'), on_delete=models.CASCADE)
    comment=models.TextField()
    rating=models.FloatField(default=0)
    date=models.DateField( auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
class Cupon(models.Model):
    code = models.CharField( max_length=50,unique=True)  
    valid_from=models.DateField()
    valid_to=models.DateField()
    discaunt=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(80)])
    active=models.BooleanField(default=False)
    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name='Add To Cupon Code'
    
class Csttt(models.Model):
    code = models.CharField( max_length=50,unique=True)  
    valid_from=models.DateField()
    valid_to=models.DateField()
    discaunt=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(80)])
    active=models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    
class spdf(models.Model):
    code = models.CharField( max_length=50,unique=True)  
    valid_from=models.DateField()
    valid_to=models.DateField()
    discaunt=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(80)])
    active=models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    
    
    
class hhhh(models.Model):
    code = models.CharField( max_length=50,unique=True)  
    valid_from=models.DateField()
    valid_to=models.DateField()
    discaunt=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(80)])
    active=models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name='Add To Cupon Code'
        
class OrderPlaced(models.Model):
    PAYMENT_GATEWAY=(
        ('Cash On Delivary','Cash On Dalivary'),
        ('Bikash','Bikash')
    )
    user=models.ForeignKey(User, verbose_name=("User Name"), on_delete=models.CASCADE)
    product=models.ForeignKey(Product, verbose_name=("Product"), on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1,verbose_name='Product Quantity')
    payment=models.CharField(choices=PAYMENT_GATEWAY, max_length=50,blank=True,null=True)
    
    first_name=models.CharField( max_length=50)
    last_name=models.CharField( max_length=50)
    country=models.CharField( max_length=50)
    address1=models.CharField( max_length=50)
    address2=models.CharField( max_length=50)
    city=models.CharField( max_length=50)
    zip=models.CharField( max_length=50)
    phone=models.CharField( max_length=50)
    email=models.EmailField( max_length=254)
    
    
    
    def __str__(self):
        return f'{self.user.username}'
    
    '''def is_fully_filled(self):
        field_names=[f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value= getattr(self,field_name)
            if value is None or value == '':
                return False
            
        return True
            '''
    
class Contract(models.Model):
    user=models.ForeignKey(User,  on_delete=models.CASCADE)
    names=models.CharField( max_length=50,blank=True,null=True)
    email=models.EmailField( max_length=254)
    comment=models.TextField()
    
    
    def __str__(self):
        return f'{self.user.username}'
    
    class Meta:
        verbose_name='Contract sm'
    
class SMS(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    mnb = models.CharField(max_length=50, null=True, blank=True)

    mkl=models.EmailField( max_length=254,null=True, blank=True)
    cmm=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}'
    
class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    date=models.DateField( auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username}'


class Subscribe(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    email=models.EmailField(max_length=254,blank=True,null=True)
    date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username}'
    