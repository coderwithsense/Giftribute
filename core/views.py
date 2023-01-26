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

class SearchResults(ListView):
    model = Item
    context_object_name = "items"
    paginate_by = 10
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
    # def get(self, *args, **kwargs):
    #     try:
    #         order = Order.objects.get(user=self.request.user, ordered=False)
    #         context = {
    #             'object': order,
    #         }
    #         return render(self.request, "checkout.html", context=context)
    #     except ObjectDoesNotExist:
    #         messages.error(self.request, "You do not have anything in cart")
    #         return redirect("/")

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
                order.ordered = True
                order.save()
                return redirect("core:thank-you")
            print("DONEEEE")
            messages.warning(self.request, "Something Went Wrong")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "Something Went Wrong")
            return redirect('core:order-summary')

class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

# class SearchResultsList(ListView):
#     model = Item
#     context_object_name = "object"
#     template_name = "search.html"

#     def get_queryset(self):
#         query = self.request.GET.get("q")
#         return Quote.objects.filter(quote__search=query)

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

def thank_you(request):
    return render(request, "thank_you.html")

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