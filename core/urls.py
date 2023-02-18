from django.urls import path
from .views import HomeView, OrderSummaryView, ItemDetailView, checkout, view_profile, orders_view, add_to_cart, remove_from_cart, SearchResults, confirm_order, thank_you
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='item-list'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkout.as_view(), name='checkout-page'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('confirm-order/', confirm_order, name='confirm-order'),
    path('thank_you/', thank_you, name="thank-you"),
    path('profile/', view_profile, name="profile-view"),
    path('orders/', orders_view, name="orders-view"),

    path('search/', SearchResults.as_view(), name="search_results"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)