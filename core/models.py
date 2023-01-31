from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify
from PIL import Image 
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
import uuid

CATEGORY_CHOICES = (
    ('M', 'Men'),
    ('W', 'Women'),
    ('C', 'Children')
)

STARCHOICES = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5)
)

HAMPER_CHOICES = (
    ('C', 'Chocolates'),
    ('I', 'Another Item')
)

class images(models.Model):
    name = models.CharField(max_length=10, default="unknown ")
    image = models.ImageField(upload_to = 'media/products/')

    def __str__(self):
        return self.image.url

class Reviews(models.Model):
    name = models.CharField(max_length=15, default="Unknown")
    date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=200)
    showOnItem = models.BooleanField(default=True)
    stars = models.CharField(choices=STARCHOICES, max_length=2, default=5)

    def __str__(self):
        return self.text

class category(models.Model):
    category = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.category

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField() 
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(
        default='',
        editable=True,
        blank=True)
    image = models.ManyToManyField(images)
    description = models.TextField(max_length=3000)
    long_description = models.TextField(max_length=2000)
    additional_info = models.TextField(max_length=2000, blank=True, null=True, default="No additional info given by the seller")
    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })
    
    def save(self, *args, **kwargs):
        value = uuid.uuid1()
        self.slug = slugify(value, allow_unicode=True)

        # # image resizing before upload
        # img = Image.open(self.image)
        # print(self.image)
        # output_size = (500, 500)
        # img.thumbnail(output_size)
        # img.save(self.image)
        super().save(*args, **kwargs)


class ReviewAttribute(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    reviews = models.ManyToManyField(Reviews)

    def __str__(self):
        return f"{self.item}"

# hamper and basket
class basket(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'media/baskets/', default="media/baskets/500X500.png")
    price = models.FloatField()

    def __str__(self):
        return self.name

class hamperProduct(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=35, choices=HAMPER_CHOICES)
    image = models.ImageField(upload_to = 'media/uploads/', default="media/uploads/500X500.png")
    price = models.FloatField()
    description = models.CharField(max_length=50, default="No description for this product")

    def __str__(self):
        return self.name

class hamper(models.Model):
    name = models.CharField(max_length=20, default="Gift Hamper")
    item = models.ManyToManyField(hamperProduct)
    slug = models.SlugField(
        default='',
        editable=True,
        blank=True)
    basket = models.ForeignKey(basket, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = uuid.uuid1()
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    

class hamperItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    hamper = models.ManyToManyField(hamper)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.hamper.name}"


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_saved_amount(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if(self.item.discount_price):
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    # hamper = models.ManyToManyField(hamperItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=25, blank=True, null=True)
    apartment_address =  models.CharField(max_length=1000, blank=True, null=True)
    street_address = models.CharField(max_length=1000, blank=True, null=True)
    country =  models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    zip =  models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username