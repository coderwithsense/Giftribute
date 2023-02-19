from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from .models import Item, Order, OrderItem, hamper, BillingAddress
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .forms import checkoutForm
from .utils import make_payment, shipping_order, get_payment
from datetime import datetime

# utils
def get_order_details(order):
    order_items = []
    for item in order.items.all():
        order_items.append({
            "name": item.item.title,
            "sku": item.item.slug,
            "units": item.quantity,
            "selling_price": str(item.item.price),
            "discount": "",
            "tax": "",
            "hsn": ""
        })
    print(order_items)
    return order_items

class SearchResults(ListView):
    model = Item
    context_object_name = "items"
    # paginate_by = 10
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Item.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(long_description__icontains=query)
        )

class HomeView(ListView):
    model = Item
    paginate_by = 20
    template_name = "home-page.html"

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, "order-summary.html", context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have anything in cart")
            return redirect("/")

class checkout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = checkoutForm()
            context = {
                'form': form,
                'object': order,
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have anything in cart")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = checkoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                surname = form.cleaned_data.get('surname')
                email = form.cleaned_data.get('email')
                mobile = form.cleaned_data.get('mobile')
                apartment_address = form.cleaned_data.get('apartment_address')
                street_address = form.cleaned_data.get('street_address')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')
                billing_address = BillingAddress(
                    user = self.request.user,
                    name = name,
                    surname = surname,
                    email = email, 
                    mobile = mobile,
                    apartment_address = apartment_address,
                    street_address = street_address,
                    country = country,
                    city = city,
                    state = state,
                    zip = zip,
                )
                billing_address.save()
                order.BillingAddress = billing_address
                response = make_payment(amount=order.get_total(), comment=f"Order for {name} {surname} of amount {order.get_total()}", name=name, email=email, phone="6358740371", redirect_url=f"http://{self.request.META['HTTP_HOST']}/thank_you/")
                order.payment_id = response['payment_request']['id']
                order.ordered_date = datetime.now()
                print(response)
                order.save()

                order_items = get_order_details(order=order)
                shipping_response = shipping_order(order.order_id, order_date=datetime.now().strftime("%Y-%m-%d %H:%M"), name=name, surname=surname, address1=apartment_address, address2=street_address, city=city, pincode=zip, country='India', state=state, email_addr=email, phone_number="6358740371", order_items=order_items, amount_total=order.get_total(), length=10, breadth=10, height=10, weight=0.4)
                print(shipping_response)

                if 'payment_request' in response:
                    long_url = response['payment_request']['longurl']
                    return redirect(long_url)
                else:
                    # Handle the error condition
                    print(response)
                return redirect(long_url)
            print("DONEEEE")
            messages.warning(self.request, "Something Went Wrong")
            return redirect('core:checkout-page')
        except ObjectDoesNotExist:
            messages.warning(self.request, "Something Went Wrong")
            return redirect('core:order-summary')

def thank_you(request):
    # update COD to prepaid if done
    # update paid in order
    payment_request_id = request.GET.get('payment_request_id')
    payment_status = get_payment(payment_request_id)['success']
    order = get_object_or_404(Order, payment_id=payment_request_id)
    if payment_status:
        order.paid = True
        order.ordered = True
        order.save()
    context = {
        'payment_request_id': payment_request_id,
        'order': order,
    }
    return render(request, "thank_you.html", context=context)

class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

@login_required
def view_profile(request):
    context={
        'user': request.user
    }
    return render(request, 'profile.html', context)

@login_required
def orders_view(request):
    orders = Order.objects.filter(ordered=True, user=request.user)
    # orders = get_object_or_404(Order, ordered=True, user=request.user)
    context={
        'orders': orders
    }
    return render(request, 'orders.html', context)

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:product", slug=slug)

@login_required
def confirm_order(request):
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        order.ordered = True
        order.ordered_date = timezone.now()

        return redirect("core:thank-you")
    return redirect("core:checkout-page")



@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)