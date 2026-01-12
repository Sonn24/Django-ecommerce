from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from autoslug import AutoSlugField



CATEGORY_CHOICES = (
    ('BR', 'Branded'),
    ('PM', 'Photo Mount'),
    ('PK', 'Package'),
)


SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('A0', 'A0'),
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('A3+', 'A3+'),
    ('A3', 'A3'),
    ('A4', 'A4'),
    ('A5', 'A5'),
)

LABEL_CHOICES = (
    ('N', 'New'),
    ('B', 'Best Seller'),
    ('O', 'Offer'),
)
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


from django.db import models
from django.urls import reverse

CATEGORY_CHOICES = (
    ('BR', 'Branded'),
    ('PM', 'Photo Mount'),
    ('PK', 'Package'),
    ('DS', 'Design'),
)

SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('A0', 'A0'),
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('A3+', 'A3+'),
    ('A3', 'A3'),
    ('A4', 'A4'),
    ('A5', 'A5'),
)


LABEL_CHOICES = (
    ('N', 'New'),
    ('B', 'Best Seller'),
    ('O', 'Offer'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

 
    minimum_quantity = models.PositiveIntegerField(default=1)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug': self.slug})


# ✅ Photo Mount Sizes
class ItemSize(models.Model):
    item = models.ForeignKey("Item", related_name="sizes", on_delete=models.CASCADE)
    size = models.CharField(choices=SIZE_CHOICES, max_length=4)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.item.title} - {self.size}"


# ✅ Branded Colors / Teams
class ItemColor(models.Model):
    item = models.ForeignKey("Item", related_name="colors", on_delete=models.CASCADE)
    color_or_team = models.CharField(max_length=50)  # e.g. Red, Chelsea, Man United

    def __str__(self):
        return f"{self.item.title} - {self.color_or_team}"



class OrderItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Item', 
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'item', 'size', 'color', 'ordered')
        ordering = ['item']

    def __str__(self):
        return f"{self.quantity} x {self.item.title} ({self.size or '-'}, {self.color or '-'})"

    # Total price without discount
    def get_total_item_price(self):
        return self.quantity * (self.price if self.price else self.item.price)

    # Total price with discount (if any)
    def get_total_discount_item_price(self):
        if self.item.discount_price:
            return self.quantity * (self.price if self.price else self.item.discount_price)
        return self.get_total_item_price()

    # Amount saved due to discount
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    # Final price for checkout
    def get_final_price(self):
        return self.get_total_discount_item_price() if self.item.discount_price else self.get_total_item_price()




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)





class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
    

class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
    

class ServiceModel(models.Model):
    icon = models.CharField(max_length=100)
    service = models.CharField(max_length=50)
    icon_desc = models.CharField(max_length=100,default='')
    slug = AutoSlugField(populate_from ='service', unique=True,null = True,default=None)

    def __str__(self):
        return self.service
    
class ServiceItem(models.Model):
    service = models.ForeignKey(ServiceModel, related_name='service_items', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description[:50]

class AboutModel(models.Model):
    
    image = models.ImageField(upload_to='img/',max_length=100) 
    tagline = models.TextField() 
    para1 = models.TextField()
    para2 = models.TextField(default='default_value')

    def __str__(self):
        return self.tagline
    
class ListItem(models.Model):
    about = models.ForeignKey(AboutModel, related_name='list_items', on_delete=models.CASCADE)
    icon = models.CharField(max_length=50)
    icon_des = models.CharField(max_length=250)

    def __str__(self):
        return self.icon_des[:50]
     
class ClientModel(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='client/', max_length=100)

    def __str__(self):
        return self.title

class Features(models.Model):
    icon = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title    

class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ('customized-branding', 'Customized-branding'),
        ('graphics-design', 'Graphics-design'),
        ('large-format-printing', 'Large-format-printing'),
        ('photography-videography', 'Photography-videography'),
    ]
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='portfolio/', max_length=100)

    def __str__(self):
        return self.title
    
class Portfolio_details(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    project_date = models.DateField()
    project_url = models.URLField()
    tagline = models.TextField(default='')
    description = models.TextField()
    #images = models.JSONField(default= dict)  # Storing image URLs as JSON list

    def __str__(self):
        return self.title


class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(Portfolio_details, related_name='portfolio_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio_images/')

    def __str__(self):
        return self.image.url
    

class Header(models.Model):
    site_name = models.CharField(max_length=50)
    line1 = models.CharField(max_length=150)
    line2 = models.CharField(max_length=150)

    def __str__(self):
        return self.site_name
class Hero(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class HeroImage(models.Model):
    hero = models.ForeignKey(Hero, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hero_images/')

    def __str__(self):
        return f"Image for {self.hero.title}"

class Footer(models.Model):
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    newsletter =  models.CharField(max_length=200)

    def __str__(self):
        return self.address
    
class Social(models.Model):
    icon = models.CharField(max_length=100)
    link = models.CharField(max_length=300, default= '#')

    def __str__(self):
        return self.icon
    
      