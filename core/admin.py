from django.contrib import admin

from .models import Item, Order, OrderItem, Reviews, ReviewAttribute, basket, hamperProduct, hamper, hamperItem, images, category, BillingAddress


admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Reviews)
admin.site.register(ReviewAttribute)
admin.site.register(basket)
admin.site.register(hamperProduct)
admin.site.register(hamper)
admin.site.register(hamperItem)
admin.site.register(images)
admin.site.register(category)
admin.site.register(BillingAddress)
