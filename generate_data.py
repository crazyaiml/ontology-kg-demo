"""
Generate sample sales data for the demo
"""
import pandas as pd
import random
from datetime import datetime, timedelta
import json

def generate_sales_data(num_records=500):
    """Generate realistic sales data"""
    
    # Define data components
    products = [
        {"id": "P001", "name": "Laptop Pro 15", "category": "Electronics", "subcategory": "Computers", "price": 1299.99},
        {"id": "P002", "name": "Wireless Mouse", "category": "Electronics", "subcategory": "Accessories", "price": 29.99},
        {"id": "P003", "name": "USB-C Hub", "category": "Electronics", "subcategory": "Accessories", "price": 49.99},
        {"id": "P004", "name": "Monitor 27inch", "category": "Electronics", "subcategory": "Displays", "price": 399.99},
        {"id": "P005", "name": "Mechanical Keyboard", "category": "Electronics", "subcategory": "Accessories", "price": 129.99},
        {"id": "P006", "name": "Office Chair Premium", "category": "Furniture", "subcategory": "Seating", "price": 449.99},
        {"id": "P007", "name": "Standing Desk", "category": "Furniture", "subcategory": "Desks", "price": 599.99},
        {"id": "P008", "name": "Desk Lamp LED", "category": "Furniture", "subcategory": "Lighting", "price": 79.99},
        {"id": "P009", "name": "Bookshelf", "category": "Furniture", "subcategory": "Storage", "price": 199.99},
        {"id": "P010", "name": "Tablet 10inch", "category": "Electronics", "subcategory": "Mobile Devices", "price": 499.99},
    ]
    
    customers = [
        {"id": "C001", "name": "Acme Corp", "type": "Enterprise", "region": "North America", "industry": "Technology"},
        {"id": "C002", "name": "TechStart Inc", "type": "SMB", "region": "North America", "industry": "Technology"},
        {"id": "C003", "name": "Global Solutions", "type": "Enterprise", "region": "Europe", "industry": "Consulting"},
        {"id": "C004", "name": "Design Studio", "type": "SMB", "region": "Europe", "industry": "Creative"},
        {"id": "C005", "name": "Finance Plus", "type": "Mid-Market", "region": "Asia", "industry": "Finance"},
        {"id": "C006", "name": "Retail Giant", "type": "Enterprise", "region": "North America", "industry": "Retail"},
        {"id": "C007", "name": "Startup Hub", "type": "SMB", "region": "Asia", "industry": "Technology"},
        {"id": "C008", "name": "Manufacturing Co", "type": "Mid-Market", "region": "Europe", "industry": "Manufacturing"},
        {"id": "C009", "name": "Healthcare Systems", "type": "Enterprise", "region": "North America", "industry": "Healthcare"},
        {"id": "C010", "name": "Education First", "type": "Mid-Market", "region": "Asia", "industry": "Education"},
    ]
    
    sales_reps = [
        {"id": "SR001", "name": "John Smith", "region": "North America", "experience_years": 5},
        {"id": "SR002", "name": "Emma Johnson", "region": "Europe", "experience_years": 3},
        {"id": "SR003", "name": "Michael Chen", "region": "Asia", "experience_years": 7},
        {"id": "SR004", "name": "Sarah Williams", "region": "North America", "experience_years": 4},
        {"id": "SR005", "name": "David Brown", "region": "Europe", "experience_years": 6},
    ]
    
    # Generate sales records
    sales_data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        customer = random.choice(customers)
        product = random.choice(products)
        
        # Sales rep from matching region
        matching_reps = [rep for rep in sales_reps if rep["region"] == customer["region"]]
        sales_rep = random.choice(matching_reps) if matching_reps else random.choice(sales_reps)
        
        # Generate date
        days_offset = random.randint(0, 365)
        sale_date = start_date + timedelta(days=days_offset)
        
        # Generate quantity (more for enterprise customers)
        if customer["type"] == "Enterprise":
            quantity = random.randint(10, 50)
        elif customer["type"] == "Mid-Market":
            quantity = random.randint(5, 20)
        else:
            quantity = random.randint(1, 10)
        
        # Calculate revenue
        revenue = product["price"] * quantity
        
        # Add discount for large orders
        discount_percentage = 0
        if revenue > 10000:
            discount_percentage = random.choice([10, 15, 20])
        elif revenue > 5000:
            discount_percentage = random.choice([5, 10])
        
        final_revenue = revenue * (1 - discount_percentage / 100)
        
        # Status
        status = random.choices(
            ["Completed", "Pending", "Cancelled"],
            weights=[0.85, 0.10, 0.05]
        )[0]
        
        sales_data.append({
            "sale_id": f"S{str(i+1).zfill(4)}",
            "date": sale_date.strftime("%Y-%m-%d"),
            "customer_id": customer["id"],
            "customer_name": customer["name"],
            "customer_type": customer["type"],
            "customer_region": customer["region"],
            "customer_industry": customer["industry"],
            "product_id": product["id"],
            "product_name": product["name"],
            "product_category": product["category"],
            "product_subcategory": product["subcategory"],
            "unit_price": product["price"],
            "quantity": quantity,
            "gross_revenue": revenue,
            "discount_percentage": discount_percentage,
            "net_revenue": final_revenue,
            "sales_rep_id": sales_rep["id"],
            "sales_rep_name": sales_rep["name"],
            "sales_rep_experience": sales_rep["experience_years"],
            "status": status
        })
    
    # Create DataFrame
    df = pd.DataFrame(sales_data)
    
    # Save to CSV
    df.to_csv("data/sales_data.csv", index=False)
    
    # Save metadata
    metadata = {
        "products": products,
        "customers": customers,
        "sales_reps": sales_reps
    }
    
    with open("data/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Generated {num_records} sales records")
    print(f"\nData summary:")
    print(f"Total Revenue: ${df['net_revenue'].sum():,.2f}")
    print(f"Average Deal Size: ${df['net_revenue'].mean():,.2f}")
    print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
    print(f"\nFiles saved:")
    print("  - data/sales_data.csv")
    print("  - data/metadata.json")
    
    return df, metadata

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    generate_sales_data(500)
