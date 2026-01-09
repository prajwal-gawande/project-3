from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from config import config
from models import db, Category, Test, Package, Location, Patient, Booking, BookingItem
from datetime import datetime, date
import os
import random
import string

app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize database
db.init_app(app)


# Helper functions
def generate_booking_number():
    """Generate unique booking number"""
    prefix = 'APL'
    random_part = ''.join(random.choices(string.digits, k=8))
    return f"{prefix}{random_part}"


def get_cart():
    """Get cart from session"""
    return session.get('cart', [])


def save_cart(cart):
    """Save cart to session"""
    session['cart'] = cart
    session.modified = True


def calculate_cart_total(cart):
    """Calculate total amount for cart items"""
    total = 0
    for item in cart:
        if item['type'] == 'test':
            test = Test.query.get(item['id'])
            if test:
                total += test.price
        elif item['type'] == 'package':
            package = Package.query.get(item['id'])
            if package:
                total += package.price
    return total


# Routes
@app.route('/')
def index():
    featured_packages = Package.query.limit(4).all()
    popular_tests = Test.query.limit(6).all()
    cart_count = len(session.get('cart', []))
    return render_template('index.html', 
                         featured_packages=featured_packages,
                         popular_tests=popular_tests,
                         cart_count=cart_count)

@app.route('/upload-prescription', methods=['GET', 'POST'])
def upload_prescription():
    cart_count = len(session.get('cart', []))
    if request.method == 'POST':
        # In a real app, file saving logic would go here
        return jsonify({'success': True, 'message': 'Prescription uploaded successfully'})
    return render_template('upload-prescription.html', cart_count=cart_count)


@app.route('/tests')
def test_listing():
    """Test listing page with filters"""
    # Get filter parameters
    category_slug = request.args.get('category')
    search_query = request.args.get('q', '').strip()
    
    # Base query
    query = Test.query
    
    # Apply category filter
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
    
    # Apply search filter
    if search_query:
        query = query.filter(Test.name.ilike(f'%{search_query}%'))
    
    tests = query.all()
    categories = Category.query.all()
    
    cart = get_cart()
    cart_count = len(cart)
    
    return render_template('test-listing.html',
                         tests=tests,
                         categories=categories,
                         selected_category=category_slug,
                         search_query=search_query,
                         cart_count=cart_count)


@app.route('/test/<slug>')
def test_details(slug):
    """Individual test details page"""
    test = Test.query.filter_by(slug=slug).first_or_404()
    related_tests = Test.query.filter_by(category_id=test.category_id).filter(Test.id != test.id).limit(3).all()
    
    cart = get_cart()
    cart_count = len(cart)
    
    return render_template('test-details.html',
                         test=test,
                         related_tests=related_tests,
                         cart_count=cart_count)


@app.route('/packages')
def package_listing():
    """Package listing page"""
    packages = Package.query.all()
    
    cart = get_cart()
    cart_count = len(cart)
    
    return render_template('package-listing.html',
                         packages=packages,
                         cart_count=cart_count)


@app.route('/package/<slug>')
def package_details(slug):
    """Package details page"""
    package = Package.query.filter_by(slug=slug).first_or_404()
    
    cart = get_cart()
    cart_count = len(cart)
    
    return render_template('package-details.html',
                         package=package,
                         cart_count=cart_count)


@app.route('/cart')
def cart_page():
    """Shopping cart page"""
    cart = get_cart()
    cart_items = []
    
    for item in cart:
        if item['type'] == 'test':
            test = Test.query.get(item['id'])
            if test:
                cart_items.append({
                    'type': 'test',
                    'id': test.id,
                    'name': test.name,
                    'price': test.price,
                    'original_price': test.original_price,
                    'discount': test.discount
                })
        elif item['type'] == 'package':
            package = Package.query.get(item['id'])
            if package:
                cart_items.append({
                    'type': 'package',
                    'id': package.id,
                    'name': package.name,
                    'price': package.price,
                    'original_price': package.original_price,
                    'discount': package.discount
                })
    
    total = calculate_cart_total(cart)
    cart_count = len(cart)
    
    return render_template('cart.html',
                         cart_items=cart_items,
                         total=total,
                         cart_count=cart_count)


@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    item_type = data.get('type')  # 'test' or 'package'
    item_id = data.get('id')
    
    if not item_type or not item_id:
        return jsonify({'success': False, 'message': 'Invalid request'}), 400
    
    cart = get_cart()
    
    # Check if item already in cart
    for item in cart:
        if item['type'] == item_type and item['id'] == item_id:
            return jsonify({'success': False, 'message': 'Item already in cart'}), 400
    
    # Add to cart
    cart.append({'type': item_type, 'id': item_id})
    save_cart(cart)
    
    return jsonify({'success': True, 'message': 'Item added to cart', 'cart_count': len(cart)})


@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.get_json()
    item_type = data.get('type')
    item_id = data.get('id')
    
    if not item_type or not item_id:
        return jsonify({'success': False, 'message': 'Invalid request'}), 400
    
    cart = get_cart()
    cart = [item for item in cart if not (item['type'] == item_type and item['id'] == item_id)]
    save_cart(cart)
    
    return jsonify({'success': True, 'message': 'Item removed from cart', 'cart_count': len(cart)})


@app.route('/booking')
def booking_page():
    """Booking form page"""
    cart = get_cart()
    
    if not cart:
        return redirect(url_for('index'))
    
    cart_items = []
    for item in cart:
        if item['type'] == 'test':
            test = Test.query.get(item['id'])
            if test:
                cart_items.append({
                    'type': 'test',
                    'id': test.id,
                    'name': test.name,
                    'price': test.price
                })
        elif item['type'] == 'package':
            package = Package.query.get(item['id'])
            if package:
                cart_items.append({
                    'type': 'package',
                    'id': package.id,
                    'name': package.name,
                    'price': package.price
                })
    
    total = calculate_cart_total(cart)
    locations = Location.query.filter_by(is_active=True).all()
    cart_count = len(cart)
    
    return render_template('booking.html',
                         cart_items=cart_items,
                         total=total,
                         locations=locations,
                         cart_count=cart_count)


@app.route('/booking/submit', methods=['POST'])
def submit_booking():
    """Submit booking"""
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age = request.form.get('age')
        gender = request.form.get('gender')
        address = request.form.get('address')
        city = request.form.get('city')
        pincode = request.form.get('pincode')
        location_id = request.form.get('location_id')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        special_instructions = request.form.get('special_instructions', '')
        
        # Validate required fields
        if not all([name, phone, age, gender, address, city, pincode, appointment_date, appointment_time]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Get cart
        cart = get_cart()
        if not cart:
            return jsonify({'success': False, 'message': 'Cart is empty'}), 400
        
        # Create or get patient
        patient = Patient.query.filter_by(phone=phone).first()
        if not patient:
            patient = Patient(
                name=name,
                email=email,
                phone=phone,
                age=int(age),
                gender=gender,
                address=address,
                city=city,
                pincode=pincode
            )
            db.session.add(patient)
            db.session.flush()
        
        # Create booking
        total_amount = calculate_cart_total(cart)
        booking_number = generate_booking_number()
        
        booking = Booking(
            booking_number=booking_number,
            patient_id=patient.id,
            location_id=int(location_id) if location_id else None,
            appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d').date(),
            appointment_time=appointment_time,
            total_amount=total_amount,
            status='confirmed',
            payment_status='pending',
            special_instructions=special_instructions
        )
        db.session.add(booking)
        db.session.flush()
        
        # Create booking items
        for item in cart:
            if item['type'] == 'test':
                test = Test.query.get(item['id'])
                if test:
                    booking_item = BookingItem(
                        booking_id=booking.id,
                        item_type='test',
                        item_id=test.id,
                        item_name=test.name,
                        price=test.price
                    )
                    db.session.add(booking_item)
            elif item['type'] == 'package':
                package = Package.query.get(item['id'])
                if package:
                    booking_item = BookingItem(
                        booking_id=booking.id,
                        item_type='package',
                        item_id=package.id,
                        item_name=package.name,
                        price=package.price
                    )
                    db.session.add(booking_item)
        
        db.session.commit()
        
        # Clear cart
        save_cart([])
        
        return jsonify({
            'success': True,
            'message': 'Booking confirmed successfully',
            'booking_number': booking_number,
            'redirect_url': url_for('confirmation', booking_number=booking_number)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/confirmation/<booking_number>')
def confirmation(booking_number):
    """Booking confirmation page"""
    booking = Booking.query.filter_by(booking_number=booking_number).first_or_404()
    
    return render_template('confirmation.html',
                         booking=booking,
                         cart_count=0)


# API Routes
@app.route('/api/tests')
def api_tests():
    """Get tests with filters (JSON)"""
    category_slug = request.args.get('category')
    search_query = request.args.get('q', '').strip()
    
    query = Test.query
    
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
    
    if search_query:
        query = query.filter(Test.name.ilike(f'%{search_query}%'))
    
    tests = query.all()
    return jsonify([test.to_dict() for test in tests])


@app.route('/api/packages')
def api_packages():
    """Get packages (JSON)"""
    packages = Package.query.all()
    return jsonify([package.to_dict() for package in packages])


@app.route('/api/locations')
def api_locations():
    """Get center locations (JSON)"""
    city = request.args.get('city')
    
    query = Location.query.filter_by(is_active=True)
    
    if city:
        query = query.filter_by(city=city)
    
    locations = query.all()
    return jsonify([location.to_dict() for location in locations])


@app.route('/api/search')
def api_search():
    """Search tests and packages (JSON)"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'tests': [], 'packages': []})
    
    tests = Test.query.filter(Test.name.ilike(f'%{query}%')).limit(5).all()
    packages = Package.query.filter(Package.name.ilike(f'%{query}%')).limit(5).all()
    
    return jsonify({
        'tests': [test.to_dict() for test in tests],
        'packages': [package.to_dict() for package in packages]
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
