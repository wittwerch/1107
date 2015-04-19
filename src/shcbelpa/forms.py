from cartridge.shop.forms import OrderForm
from cartridge.shop.models import Order

class CustomOrderForm(OrderForm):

    class Meta:
        model = Order
        fields = (["billing_detail_first_name",
                   "billing_detail_last_name",
                   "billing_detail_street",
                   "billing_detail_postcode",
                   "billing_detail_city",
                   "billing_detail_phone",
                   "billing_detail_email",
                   "additional_instructions",
                   "discount_code"])
