from init_db import product_registry

from init_db import product_registry

def marketdisplay():
    print("\n" + "="*45)
    print(f"{'PRODUCT':<15} | {'PRODUCER':<20} | {'PRICE':<8}")
    print("-" * 45)

    if not product_registry:
        print("No companies are currently producing goods.")
    else:
        for p_name, details in product_registry.items():
            print(f"{details['name']:<15} | {details['producer']:<20} | R{details['price']:<8}")
    
    print("="*45 + "\n")
    
def main():
    marketdisplay()

if __name__ == "__main__":
    main()