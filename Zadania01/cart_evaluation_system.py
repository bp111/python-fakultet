class Product:
    def __init__(self, stock_keeping_unit, name, category, unit_price):
        self.stock_keeping_unit = stock_keeping_unit
        self.name = name
        self.category = category
        self.unit_price = unit_price               
        self.validate()

    def validate(self):
        if self.unit_price < 0:
            raise ValueError(f"{self.name} must have a non-negative price!")                   

class CartItem:    
    def __init__(self, product, quantity, vat_rate):
        self.product = product
        self.quantity = quantity
        self.vat_rate = vat_rate     # for example 0.23        
        self.original_unit_price = product.unit_price
        self.discounted_unit_price = product.unit_price

class BuyerData:
    def __init__(self, id_client, loyalty_level):
        self.id_client = id_client
        self.loyalty_level = loyalty_level                
        self.validate()

    def validate(self):        
        if self.loyalty_level < 0:
            raise ValueError("Loyalty level can't be negative!")
        
class Receipt:
    def __init__(self, items_info, total_net, total_vat, total_gross, total_savings):
        self.items_info = items_info
        self.total_net = total_net
        self.total_vat = total_vat
        self.total_gross = total_gross
        self.total_savings = total_savings    

    def __repr__(self):    
        return (f"<Receipt: Gross: {self.total_gross}, "
            f"Net: {self.total_net}, "
            f"Savings: {self.total_savings}, "
            f"Items: {len(self.items_info)}>")
                
# ================ DISCOUNTS ================
    
class FifteenPercentOffAllShoes:
    def __init__(self):
        self.discount_percent = 0.15        
        self.category_target = "shoes"        

    def calculate(self, cart_items, buyer):                        
        for item in cart_items:
            if item.product.category == self.category_target:                
                discount_multiplier = 1.0 - self.discount_percent
                item.discounted_unit_price *= discount_multiplier


class TwoPlusOneForMilkChocolate:
    def __init__(self):
        self.target_sku = "CHOC-1"

    def calculate(self, cart_items, buyer):        
        for item in cart_items:
            if item.product.stock_keeping_unit == self.target_sku:                
                free_items = item.quantity // 3                
                if free_items > 0:                    
                    current_total_price = item.discounted_unit_price * item.quantity                                        
                    money_saved = free_items * item.discounted_unit_price

                    new_total_price = current_total_price - money_saved
                    item.discounted_unit_price = new_total_price / item.quantity

offered_products = [
    Product("SHOE-1", "Sneakers", "shoes", 450.0),
    Product("SHOE-2", "Slippers", "shoes", 40.0),
    Product("CHOC-1", "Milk Chocolate", "chocolate", 8.0),
    Product("CHOC-2", "Dark Chocolate", "chocolate", 8.5),
]

buyers_list = [
    BuyerData(id_client=1, loyalty_level=5),
    BuyerData(id_client=2, loyalty_level=100)
]   

offered_discounts = [
    FifteenPercentOffAllShoes(),
    TwoPlusOneForMilkChocolate()
]                    

        
def generate_receipt(cart_items, buyer, active_discounts):    
    if not isinstance(cart_items, list) or not all(isinstance(i, CartItem) for i in cart_items):
        raise ValueError("cart_items must be a list of CartItem objects!")
    if not isinstance(buyer, BuyerData):
        raise ValueError("Invalid buyer data!")
        
    for discount in active_discounts:
        discount.calculate(cart_items, buyer)
    
    receipt_items_data = []
    total_net = 0.0
    total_vat = 0.0
    total_savings = 0.0

    for item in cart_items:
        # Per item calculations
        line_original_net = item.original_unit_price * item.quantity
        line_discounted_net = item.discounted_unit_price * item.quantity
        line_vat = line_discounted_net * item.vat_rate
        
        savings = line_original_net - line_discounted_net
        
        receipt_items_data.append({
            "name": item.product.name,
            "original_unit_price": item.original_unit_price,
            "final_unit_price": item.discounted_unit_price,
            "quantity": item.quantity,
            "discount_amount": savings
        })

        total_net += line_discounted_net
        total_vat += line_vat
        total_savings += savings

    total_gross = total_net + total_vat

    return Receipt(
        items_info=receipt_items_data,
        total_net=round(total_net, 2),
        total_vat=round(total_vat, 2),
        total_gross=round(total_gross, 2),
        total_savings=round(total_savings, 2)
    )          