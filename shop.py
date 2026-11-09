def delivery_cost(amount, zone):
    if type(amount) is not int:
        raise TypeError("amount must be int")
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if zone not in ("city", "region"):
        raise ValueError("unknown zone")
    if amount >= 10000:
        return 0
    return 1000 if zone == "city" else 2000


def place_order(amount, zone, save_order):
    delivery = delivery_cost(amount, zone)
    order = {
        "amount": amount,
        "zone": zone,
        "delivery": delivery,
        "total": amount + delivery,
    }
    save_order(order)
    return order
