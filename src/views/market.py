from ..database.init_db import product_registry, user_registry, update_data, company_registry, update_company_data, sync_product_registry


def effect_of_buying_on_company(product_name, price):
    """Determines how a product purchase affects the producing company."""
    product = product_registry.get(product_name)
    if not product:
        return None, None
    
    producer_id = product['producer']
    company = company_registry.get(producer_id)
    
    if company:
        # For simplicity, let's say each purchase adds the purchase price to the company's vault
        new_vault = company.vault + price
        return producer_id, new_vault
    
    return None, None

def buy_product(user_id, product_name):
    """Handles purchase validation, balance deduction, and stat boosting."""
    if product_name not in product_registry:
        print(f"Error: {product_name} not found.")
        return
    
    product = product_registry[product_name]
    price = product['price']
    stat_to_boost = product_name.lower() 
    
    user = user_registry.get(user_id)
    if not user:
        print("Error: User not found.")
        return
    
    if user.balance < price:
        print(f"Insufficient funds! Need R{price}, have R{user.balance}")
        return

    # Calculate new values
    new_balance = user.balance - price
    current_stat_val = getattr(user, stat_to_boost, 0)
    new_stat_val = current_stat_val + 10 

    # Save user changes to JSON and RAM
    update_data(
        user_id, 
        balance=new_balance, 
        **{stat_to_boost: new_stat_val}
    )

    # Apply effect to the producing company
    producer_id, new_vault = effect_of_buying_on_company(product_name, price)
    if producer_id and new_vault is not None:
        update_company_data(producer_id, vault=new_vault)
        print(f"Company {producer_id} vault updated to R{new_vault}.")
    
    print(f"✅ Purchased {product_name.capitalize()}!")
    print(f"New Balance: R{new_balance} | {stat_to_boost.capitalize()}: {new_stat_val}")
    


def marketdisplay():
    sync_product_registry()  # Ensure product data is fresh
    print("\n" + "="*55)
    print(f"{'PRODUCT':<15} | {'PRODUCER':<25} | {'PRICE':<8}")
    print("-" * 55)
    for p_name, details in product_registry.items():
        producer_id = details['producer']
        producer_obj = company_registry.get(producer_id)
        producer_name = producer_obj.name if producer_obj else producer_id
        print(f"{details['name']:<15} | {producer_name:<25} | R{details['price']:<8}")
    print("="*55 + "\n")

if __name__ == "__main__":
    # Test run
    marketdisplay()