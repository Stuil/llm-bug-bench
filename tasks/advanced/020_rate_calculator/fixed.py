from decimal import Decimal, ROUND_HALF_UP

def calculate_discount(items, discount_rate):
    total = Decimal("0.00")
    for price, quantity in items:
        item_total = Decimal(str(price)) * Decimal(str(quantity))
        item_total = item_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total += item_total
    discount = total * Decimal(str(discount_rate))
    discount = discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(total - discount)
