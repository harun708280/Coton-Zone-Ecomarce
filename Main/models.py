from django.db import models
from django.contrib.auth.models import User
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
        return str(self.id)
    
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
    
    