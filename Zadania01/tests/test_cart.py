# Run with 'pytest -s' for debug info
from cart_evaluation_system import *
import pytest

def test_discounts_shoe_choc():        
    cart = [
        CartItem(offered_products[0], quantity = 1, vat_rate = 0.23),
        CartItem(offered_products[2], quantity = 3, vat_rate = 0.23)
    ]

    buyer = buyers_list[0]

    receipt = generate_receipt(cart, buyer, offered_discounts)
    print(repr(receipt))

    expected_net = 382.5 + 16.0
    expected_vat = 87.975 + 3.68
    expected_gross = expected_net + expected_vat
    expected_savings = 67.5 + 8.0

    assert receipt.total_net == pytest.approx(expected_net, 0.01)
    assert receipt.total_savings == pytest.approx(expected_savings, 0.01)
    assert receipt.total_gross == pytest.approx(490.155, 0.01)

    names = [item['name'] for item in receipt.items_info]
    assert "Sneakers" in names
    assert "Milk Chocolate" in names