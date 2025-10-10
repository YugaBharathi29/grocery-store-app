"""
Add sample data to existing database
"""

import os
from app import app, db, Category, Product

def add_sample_data():
    with app.app_context():
        print("🚀 Adding sample data...")
        
        # Sample Categories
        categories_data = [
            {
                'name': 'Vegetables',
                'description': 'Fresh farm vegetables',
                'image': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400'
            },
            {
                'name': 'Fruits',
                'description': 'Fresh seasonal fruits',
                'image': 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=400'
            },
            {
                'name': 'Dairy',
                'description': 'Milk and dairy products',
                'image': 'https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=400'
            },
            {
                'name': 'Snacks',
                'description': 'Chips, cookies and snacks',
                'image': 'https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=400'
            },
            {
                'name': 'Beverages',
                'description': 'Drinks and beverages',
                'image': 'https://images.unsplash.com/photo-1437418747212-8d9709afab22?w=400'
            },
            {
                'name': 'Bakery',
                'description': 'Bread and bakery items',
                'image': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            # Check if category already exists
            existing_cat = Category.query.filter_by(name=cat_data['name']).first()
            if existing_cat:
                categories[cat_data['name']] = existing_cat
                print(f"  ℹ️  Category '{cat_data['name']}' already exists")
            else:
                category = Category(**cat_data)
                db.session.add(category)
                db.session.flush()
                categories[cat_data['name']] = category
                print(f"  ✅ Created category: {cat_data['name']}")
        
        # Sample Products
        products_data = [
            # Vegetables
            {'name': 'Tomato', 'description': 'Fresh red tomatoes', 'price': 40, 'stock': 100, 'category': 'Vegetables', 'image': 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=400'},
            {'name': 'Potato', 'description': 'Farm fresh potatoes', 'price': 30, 'stock': 150, 'category': 'Vegetables', 'image': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400'},
            {'name': 'Onion', 'description': 'Red onions', 'price': 35, 'stock': 120, 'category': 'Vegetables', 'image': 'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=400'},
            {'name': 'Carrot', 'description': 'Orange carrots', 'price': 45, 'stock': 80, 'category': 'Vegetables', 'image': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400'},
            
            # Fruits
            {'name': 'Apple', 'description': 'Fresh red apples', 'price': 120, 'stock': 80, 'category': 'Fruits', 'image': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400'},
            {'name': 'Banana', 'description': 'Ripe yellow bananas', 'price': 50, 'stock': 100, 'category': 'Fruits', 'image': 'https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=400'},
            {'name': 'Orange', 'description': 'Juicy oranges', 'price': 80, 'stock': 90, 'category': 'Fruits', 'image': 'https://images.unsplash.com/photo-1580052614034-c55d20bfee3b?w=400'},
            {'name': 'Mango', 'description': 'Sweet mangoes', 'price': 150, 'stock': 60, 'category': 'Fruits', 'image': 'https://images.unsplash.com/photo-1605027990121-cbae9d46301b?w=400'},
            
            # Dairy
            {'name': 'Milk', 'description': 'Fresh cow milk - 1L', 'price': 60, 'stock': 50, 'category': 'Dairy', 'image': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400'},
            {'name': 'Cheese', 'description': 'Cheddar cheese - 200g', 'price': 180, 'stock': 40, 'category': 'Dairy', 'image': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400'},
            {'name': 'Yogurt', 'description': 'Greek yogurt - 500g', 'price': 80, 'stock': 60, 'category': 'Dairy', 'image': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400'},
            
            # Snacks
            {'name': 'Chips', 'description': 'Potato chips - 100g', 'price': 40, 'stock': 100, 'category': 'Snacks', 'image': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400'},
            {'name': 'Cookies', 'description': 'Chocolate cookies - 200g', 'price': 60, 'stock': 80, 'category': 'Snacks', 'image': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400'},
            
            # Beverages
            {'name': 'Orange Juice', 'description': 'Fresh orange juice - 1L', 'price': 100, 'stock': 50, 'category': 'Beverages', 'image': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400'},
            {'name': 'Coffee', 'description': 'Ground coffee - 200g', 'price': 250, 'stock': 40, 'category': 'Beverages', 'image': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400'},
            
            # Bakery
            {'name': 'Bread', 'description': 'Whole wheat bread', 'price': 40, 'stock': 80, 'category': 'Bakery', 'image': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400'},
            {'name': 'Croissant', 'description': 'Butter croissant - 4 pcs', 'price': 120, 'stock': 40, 'category': 'Bakery', 'image': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400'},
        ]
        
        for prod_data in products_data:
            category_name = prod_data.pop('category')
            
            # Check if product already exists
            existing_prod = Product.query.filter_by(name=prod_data['name']).first()
            if existing_prod:
                print(f"  ℹ️  Product '{prod_data['name']}' already exists")
            else:
                product = Product(
                    **prod_data,
                    category_id=categories[category_name].id
                )
                db.session.add(product)
                print(f"  ✅ Created product: {prod_data['name']}")
        
        db.session.commit()
        print("✅ Sample data added successfully!")

if __name__ == '__main__':
    add_sample_data()
