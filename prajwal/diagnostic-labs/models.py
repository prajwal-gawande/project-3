from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

# Association table for many-to-many relationship between packages and tests
package_tests = db.Table('package_tests',
    db.Column('package_id', db.Integer, db.ForeignKey('packages.id'), primary_key=True),
    db.Column('test_id', db.Integer, db.ForeignKey('tests.id'), primary_key=True)
)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tests = db.relationship('Test', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'icon': self.icon
        }


class Test(db.Model):
    __tablename__ = 'tests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    discount = db.Column(db.Integer, default=0)
    sample_type = db.Column(db.String(50))
    report_delivery = db.Column(db.String(50))
    home_collection = db.Column(db.Boolean, default=True)
    preparation = db.Column(db.Text)
    parameters_json = db.Column(db.Text)  # JSON string of parameters list
    test_count = db.Column(db.Integer, default=1)
    is_safe = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def parameters(self):
        if self.parameters_json:
            return json.loads(self.parameters_json)
        return []
    
    @parameters.setter
    def parameters(self, value):
        self.parameters_json = json.dumps(value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'discount': self.discount,
            'sample_type': self.sample_type,
            'report_delivery': self.report_delivery,
            'home_collection': self.home_collection,
            'preparation': self.preparation,
            'parameters': self.parameters,
            'test_count': self.test_count,
            'is_safe': self.is_safe,
            'category': self.category.to_dict() if self.category else None
        }


class Package(db.Model):
    __tablename__ = 'packages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    discount = db.Column(db.Integer, default=0)
    test_count = db.Column(db.Integer, default=0)
    legacy = db.Column(db.String(50))
    home_collection = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tests = db.relationship('Test', secondary=package_tests, lazy='subquery',
                           backref=db.backref('packages', lazy=True))
    
    def to_dict(self, include_tests=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'discount': self.discount,
            'test_count': self.test_count,
            'legacy': self.legacy,
            'home_collection': self.home_collection,
            'is_featured': self.is_featured
        }
        if include_tests:
            data['tests'] = [test.to_dict() for test in self.tests]
        return data


class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    address = db.Column(db.Text)
    pincode = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'pincode': self.pincode,
            'phone': self.phone,
            'latitude': self.latitude,
            'longitude': self.longitude
        }


class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='patient', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'gender': self.gender,
            'address': self.address,
            'city': self.city,
            'pincode': self.pincode
        }


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_number = db.Column(db.String(50), unique=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, completed, cancelled
    payment_status = db.Column(db.String(50), default='pending')  # pending, paid, failed
    special_instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    location = db.relationship('Location', backref='bookings')
    items = db.relationship('BookingItem', backref='booking', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_items=False):
        data = {
            'id': self.id,
            'booking_number': self.booking_number,
            'patient': self.patient.to_dict() if self.patient else None,
            'location': self.location.to_dict() if self.location else None,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_status': self.payment_status,
            'special_instructions': self.special_instructions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
        return data


class BookingItem(db.Model):
    __tablename__ = 'booking_items'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'test' or 'package'
    item_id = db.Column(db.Integer, nullable=False)  # ID of test or package
    item_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'item_name': self.item_name,
            'price': self.price
        }
