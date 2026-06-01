def calculate_discount(items, discount_rate):
    total = 0
    for price, quantity in items:
        total += price * quantity
    return round(total * (1 - discount_rate), 2)
