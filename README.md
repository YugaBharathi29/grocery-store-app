# Grocery Store Web Application

A full-featured grocery store web application built with Python Flask, Bootstrap, and SQLite.

## Features

### Customer Features
- **User Registration & Authentication**: Secure user registration and login system
- **Product Browsing**: Browse products by categories with search functionality
- **Shopping Cart**: Add/remove items, update quantities
- **Order Management**: Place orders, view order history, track order status
- **User Profile**: Update personal information and address
- **Responsive Design**: Mobile-friendly interface using Bootstrap

### Admin Features
- **Dashboard**: Overview of users, products, orders, and categories
- **Category Management**: Add/edit product categories with images
- **Product Management**: Add/edit products with images, pricing, and inventory
- **Order Management**: View and update order status
- **User Management**: View user details and order history

### Technical Features
- **SQLite Database**: Lightweight database for development
- **File Upload**: Image upload for categories and products
- **Email Integration**: Flask-Mail setup for notifications
- **Security**: Password hashing, session management
- **Responsive UI**: Bootstrap 5 with Font Awesome icons
- **Admin Panel**: Complete admin interface for store management

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Extract the application**
   ```bash
   unzip grocery-store-app.zip
   cd grocery-store-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`

## Default Accounts

### Admin Account
- **Username**: admin
- **Password**: admin123
- **Access**: Admin panel with full management capabilities

### Customer Account
- Register a new customer account through the registration page
- Or create additional admin accounts through the admin panel

## Configuration

### Database
The application uses SQLite database (`grocery_store.db`) which will be automatically created on first run.

### Email Configuration (Optional)
To enable email notifications, update the following in `app.py`:
```python
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
```

### Upload Directory
Product and category images are stored in `static/uploads/` directory.

## Project Structure

```
grocery-store-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Custom CSS styles
│   ├── js/
│   │   └── script.js     # Custom JavaScript
│   └── uploads/          # Uploaded images
│       ├── categories/   # Category images
│       └── products/     # Product images
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── products.html     # Products listing
    ├── product_detail.html # Product details
    ├── cart.html         # Shopping cart
    ├── checkout.html     # Checkout page
    ├── order_confirmation.html # Order confirmation
    ├── my_orders.html    # User orders
    ├── profile.html      # User profile
    └── admin/            # Admin templates
        ├── dashboard.html    # Admin dashboard
        ├── categories.html   # Category management
        ├── add_category.html # Add category
        ├── products.html     # Product management
        ├── add_product.html  # Add product
        ├── orders.html       # Order management
        └── users.html        # User management
```

## Usage

### For Customers
1. **Register/Login**: Create an account or log in
2. **Browse Products**: View products by category or search
3. **Add to Cart**: Add desired items to shopping cart
4. **Checkout**: Provide shipping address and payment method
5. **Track Orders**: View order status in "My Orders"

### For Administrators
1. **Login**: Use admin credentials (admin/admin123)
2. **Dashboard**: View overview of store statistics
3. **Manage Categories**: Add/edit product categories
4. **Manage Products**: Add/edit products with pricing and inventory
5. **Process Orders**: Update order status and view customer details
6. **User Management**: View registered users and their activity

## Database Schema

### Users Table
- User authentication and profile information
- Admin flag for administrative access

### Categories Table
- Product categories with names, descriptions, and images

### Products Table
- Product details including name, description, price, stock, and category

### Orders Table
- Order information including customer, total amount, and status

### Order Items Table
- Individual items within each order

### Cart Items Table
- Shopping cart contents for logged-in users

## Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **Session Management**: Flask sessions for user authentication
- **File Upload Validation**: Secure file upload with type checking
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- **Admin Access Control**: Decorator-based admin access restriction

## Customization

### Adding New Features
- Extend database models in `app.py`
- Create new routes and templates
- Update navigation in `base.html`

### Styling
- Modify `static/css/style.css` for custom styles
- Update Bootstrap classes in templates
- Add new Font Awesome icons as needed

### Email Templates
- Extend Flask-Mail configuration for email notifications
- Create email templates for order confirmations

## Troubleshooting

### Common Issues

1. **Database not created**: Ensure you have write permissions in the application directory
2. **Images not displaying**: Check that `static/uploads/` directory exists and has proper permissions
3. **Port already in use**: Change the port in `app.run(port=5001)` if 5000 is occupied
4. **Dependencies not installing**: Ensure you're using the correct Python version and pip

### Error Handling
The application includes basic error handling for:
- Invalid user input
- Database connection issues
- File upload errors
- Authentication failures

## Development

### Running in Debug Mode
The application runs in debug mode by default (`debug=True`). For production:
```python
app.run(debug=False, host='0.0.0.0')
```

### Adding Sample Data
You can add sample categories and products through the admin interface or by extending the database initialization code.

## License

This project is open source and available for educational and commercial use.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments in `app.py`
3. Ensure all dependencies are properly installed

## Version History

- **v1.0**: Initial release with core functionality
  - User authentication
  - Product catalog
  - Shopping cart
  - Order management
  - Admin panel
  - Responsive design

Enjoy building your grocery store application!