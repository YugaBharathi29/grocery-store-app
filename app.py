import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///grocery_store.db')

# Fix for Render's PostgreSQL URL format
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='order_items')

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_entries')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id'),)

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    categories = Category.query.all()
    products = Product.query.limit(8).all()
    return render_template('index.html', categories=categories, products=products)

@app.route('/products')
def products():
    categories = Category.query.all()
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.all()
    return render_template('products.html', products=products, categories=categories, current_category=category_id)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    related_products = Product.query.filter(Product.category_id == product.category_id, Product.id != product.id).limit(4).all()
    return render_template('product_detail.html', product=product, related_products=related_products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        user.full_name = request.form['full_name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.address = request.form['address']
        
        new_password = request.form.get('new_password')
        if new_password:
            user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)

# Cart Routes
@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    
    products = []
    total = 0
    
    for item in cart_items:
        if item.product:
            products.append({
                'product': item.product,
                'quantity': item.quantity
            })
            total += item.product.price * item.quantity
    
    return render_template('cart.html', products=products, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if product.stock < quantity:
        flash(f'Only {product.stock} items available in stock!', 'error')
        return redirect(url_for('product_detail', id=product_id))
    
    cart_item = Cart.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(
            user_id=session['user_id'],
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
@login_required
def update_cart_quantity(product_id):
    action = request.form.get('action')
    
    cart_item = Cart.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if not cart_item:
        flash('Item not found in cart.', 'error')
        return redirect(url_for('cart'))
    
    product = Product.query.get_or_404(product_id)
    
    if action == 'increase':
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            flash(f'Quantity increased for {product.name}', 'success')
        else:
            flash(f'Only {product.stock} items available in stock!', 'error')
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            flash(f'Quantity decreased for {product.name}', 'success')
        else:
            db.session.delete(cart_item)
            flash(f'{product.name} removed from cart.', 'success')
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart_item = Cart.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if cart_item:
        product_name = cart_item.product.name
        db.session.delete(cart_item)
        db.session.commit()
        flash(f'{product_name} removed from cart.', 'success')
    else:
        flash('Item not found in cart.', 'error')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    
    if not cart_items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart'))
    
    subtotal = sum(item.product.price * item.quantity for item in cart_items if item.product)
    total = subtotal + 50
    
    if request.method == 'POST':
        try:
            # Validate form data
            shipping_address = request.form.get('shipping_address', '').strip()
            payment_method = request.form.get('payment_method', '').strip()
            
            if not shipping_address:
                flash('Please enter shipping address.', 'error')
                return redirect(url_for('checkout'))
            
            if not payment_method:
                flash('Please select payment method.', 'error')
                return redirect(url_for('checkout'))
            
            # Create order
            order = Order(
                user_id=session['user_id'],
                total_amount=total,
                shipping_address=shipping_address,
                payment_method=payment_method,
                status='Pending'
            )
            db.session.add(order)
            db.session.flush()
            
            # Create order items and update stock
            for item in cart_items:
                if item.product:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=item.product.id,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                    db.session.add(order_item)
                    item.product.stock = max(0, item.product.stock - item.quantity)
            
            # Clear cart
            for item in cart_items:
                db.session.delete(item)
            
            db.session.commit()
            flash('Order placed successfully! Order ID: ' + str(order.id), 'success')
            return redirect(url_for('my_orders'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error processing order. Please try again.', 'error')
            print(f"Order error: {str(e)}")
            return redirect(url_for('checkout'))
    
    user = User.query.get(session['user_id'])
    return render_template('checkout.html', 
                          cart_items=cart_items, 
                          subtotal=subtotal, 
                          total=total, 
                          user=user)

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)

# Admin Routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_categories = Category.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_categories=total_categories,
                         recent_orders=recent_orders)

@app.route('/admin/categories')
@admin_required
def admin_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/add_category', methods=['GET', 'POST'])
@admin_required
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form.get("image_url", "").strip()
        image_file = request.files.get("image_file")
        image_filename = None

        if image_url:
            image_filename = image_url
        elif image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            path = f"categories/{filename}"
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'categories'), exist_ok=True)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], path))
            image_filename = path

        category = Category(name=name, description=description, image=image_filename)
        db.session.add(category)
        db.session.commit()

        flash('Category added successfully!', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/add_category.html')

@app.route('/admin/edit_category/<int:category_id>', methods=['GET', 'POST'])
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']
        image_url = request.form.get("image_url", "").strip()
        image_file = request.files.get("image_file")
        
        if image_url:
            category.image = image_url
        elif image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            path = f"categories/{filename}"
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'categories'), exist_ok=True)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], path))
            category.image = path
        
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/delete_category/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/products')
@admin_required
def admin_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@admin_required
def add_product():
    categories = Category.query.all()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        category_id = int(request.form['category_id'])
        
        image_url = request.form.get("image_url", "").strip()
        image_file = request.files.get("image_file")
        image_filename = None

        if image_url:
            image_filename = image_url
        elif image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            path = f"products/{filename}"
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), exist_ok=True)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], path))
            image_filename = path

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            image=image_filename
        )
        db.session.add(product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category_id = int(request.form['category_id'])
        
        image_url = request.form.get("image_url", "").strip()
        image_file = request.files.get("image_file")
        
        if image_url:
            product.image = image_url
        elif image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            path = f"products/{filename}"
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), exist_ok=True)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], path))
            product.image = path
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.form['status']
    db.session.commit()
    flash('Order status updated!', 'success')
    return redirect(url_for('admin_orders'))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.full_name = request.form['full_name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.address = request.form['address']
        user.is_admin = 'is_admin' in request.form
        
        new_password = request.form.get('new_password')
        if new_password:
            user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/edit_user.html', user=user)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == session['user_id']:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin_user = User(
                username='admin',
                email='admin@grocery.com',
                password_hash=generate_password_hash('admin123'),
                full_name='Admin User',
                phone='1234567890',
                address='Admin Address',
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created: username=admin, password=admin123")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
