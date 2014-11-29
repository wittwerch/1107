"""
http://bitofpixels.com/blog/collecting-additional-information-on-a-per-product-basis-in-cartridge/
"""

from copy import deepcopy

from django import forms
from django.db.models.signals import pre_save
from cartridge.shop.forms import AddProductForm, ADD_PRODUCT_ERRORS
from cartridge.shop.models import ProductVariation, Cart, Order, force_text, Decimal, SelectedProduct
from mezzanine.conf import settings

original_product_add_init = deepcopy(AddProductForm.__init__)
def product_add_init(self, *args, **kwargs):
    """
    Add player number to add to cart form
    """
    original_product_add_init(self, *args, **kwargs)
    if self._product and self._product.require_number:
        self.fields['player_number'] = forms.DecimalField(max_value=99, min_value=0, decimal_places=0)

AddProductForm.__init__ = product_add_init

def product_add_clean(self):
    """
    Determine the chosen variation, validate it and assign it as
    an attribute to be used in views.

    Store the student ID if it exists
    """
    if not self.is_valid():
        return
    # Posted data will either be a sku, or product options for
    # a variation.
    data = self.cleaned_data.copy()
    quantity = data.pop("quantity")
    student_id = None
    if self._product and self._product.require_number:
        player_number = data.pop("player_number")
    # Ensure the product has a price if adding to cart.
    if self._to_cart:
        data["unit_price__isnull"] = False
    error = None
    if self._product is not None:
        # Chosen options will be passed to the product's
        # variations.
        qs = self._product.variations
    else:
        # A product hasn't been given since we have a direct sku.
        qs = ProductVariation.objects
    try:
        variation = qs.get(**data)
    except ProductVariation.DoesNotExist:
        error = "invalid_options"
    else:
        # Validate stock if adding to cart.
        if self._to_cart:
            if not variation.has_stock():
                error = "no_stock"
            elif not variation.has_stock(quantity):
                error = "no_stock_quantity"
    if error is not None:
        raise forms.ValidationError(ADD_PRODUCT_ERRORS[error])
    self.variation = variation
    try:
        self.variation._player_number = player_number
    except:
        pass
    return self.cleaned_data
AddProductForm.clean = product_add_clean

def add_item_mod(self, variation, quantity):
    """
    Increase quantity of existing item if SKU matches, otherwise create
    new.
    """
    kwargs = {"sku": variation.sku, "unit_price": variation.price()}
    item, created = self.items.get_or_create(**kwargs)
    if created:
        item.description = force_text(variation)
        item.unit_price = variation.price()
        item.url = variation.product.get_absolute_url()
        try:
            item.player_number = variation._player_number
        except AttributeError:
            pass
        image = variation.image
        if image is not None:
            item.image = force_text(image.file)
        variation.product.actions.added_to_cart()
    item.quantity += quantity
    item.save()
Cart.add_item = add_item_mod

def setup(self, request):
    """
    Set order fields that are stored in the session, item_total
    and total based on the given cart, and copy the cart items
    to the order. Called in the final step of the checkout process
    prior to the payment handler being called.

    Also copies student IDs
    """
    self.key = request.session.session_key
    self.user_id = request.user.id
    for field in self.session_fields:
        if field in request.session:
            setattr(self, field, request.session[field])
    self.total = self.item_total = request.cart.total_price()
    if self.shipping_total is not None:
        self.shipping_total = Decimal(str(self.shipping_total))
        self.total += self.shipping_total
    if self.discount_total is not None:
        self.total -= Decimal(self.discount_total)
    if self.tax_total is not None:
        self.total += Decimal(self.tax_total)
    self.save()  # We need an ID before we can add related items.
    for item in request.cart:
        product_fields = [f.name for f in SelectedProduct._meta.fields] + ['player_number']
        item = dict([(f, getattr(item, f)) for f in product_fields])
        self.items.create(**item)
Order.setup = setup


def shop_order_status_handler(sender, instance, **kwargs):
    """
    Signal that listens on a order for a status change
    """
    try:
        obj = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        pass # Object is new, so field hasn't technically changed, but you may want to do something else here.
    else:
        if obj.status == 1 and instance.status == 2: # Field has changed from "Neu" to "Bezahlt"
            print "Mail sent"


pre_save.connect(shop_order_status_handler, sender=Order, weak=False, dispatch_uid="shop_order_status_handler")