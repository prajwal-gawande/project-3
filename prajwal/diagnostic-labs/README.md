# Apollo Diagnostics Clone

A comprehensive diagnostic lab booking platform inspired by Apollo Diagnostics, built with **HTML, CSS, JavaScript** frontend and **Flask + MySQL** backend using SQLAlchemy ORM.

## 🚀 Features

- **Browse Tests & Packages**: Explore diagnostic tests and health check packages
- **Advanced Filtering**: Filter tests by health conditions and categories
- **Search Functionality**: Quick search for tests and packages
- **Shopping Cart**: Add multiple tests/packages to cart
- **Complete Booking Flow**: Patient details, appointment scheduling, confirmation
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Modern UI**: Teal and magenta color scheme matching Apollo Diagnostics
- **MySQL Database**: Persistent data storage with SQLAlchemy ORM

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## 🛠️ Installation & Setup

### 1. Clone/Navigate to Project Directory

```bash
cd c:/Users/ratho/Desktop/prajwal/apollo-diagnostics-clone
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Linux/Mac**: `source venv/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

**Create MySQL Database:**

```sql
CREATE DATABASE testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Update `.env` file** (already configured with your credentials):

```
DATABASE_URL=mysql+pymysql://root:Virendra@30@localhost/testdb
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
```

### 5. Initialize Database & Seed Data

```bash
python seed_data.py
```

This will:
- Create all database tables
- Populate with 8 categories
- Add 8 sample diagnostic tests
- Add 4 health packages
- Add 5 center locations

### 6. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 📁 Project Structure

```
apollo-diagnostics-clone/
├── app.py                      # Flask application with routes
├── models.py                   # SQLAlchemy ORM models
├── config.py                   # Configuration settings
├── seed_data.py                # Database seeding script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── static/
│   ├── css/
│   │   ├── main.css           # Global styles & design system
│   │   ├── header.css         # Header & navigation
│   │   ├── homepage.css       # Homepage styles
│   │   ├── test-listing.css   # Test listing page
│   │   ├── test-details.css   # Test/package details
│   │   └── booking.css        # Cart & booking flow
│   ├── js/
│   │   ├── main.js            # Global JavaScript
│   │   ├── cart.js            # Cart management
│   │   └── booking.js         # Booking form handling
│   └── images/                # Images and icons
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Homepage
    ├── test-listing.html      # Test listing
    ├── test-details.html      # Test details
    ├── package-listing.html   # Package listing
    ├── package-details.html   # Package details
    ├── cart.html              # Shopping cart
    ├── booking.html           # Booking form
    └── confirmation.html      # Booking confirmation
```

## 🗄️ Database Models

- **Category**: Test categories (Heart, Liver, Kidney, etc.)
- **Test**: Diagnostic tests with pricing and parameters
- **Package**: Health check packages containing multiple tests
- **Location**: Diagnostic center locations
- **Patient**: Patient information
- **Booking**: Customer bookings
- **BookingItem**: Items in each booking

## 🎨 Design System

### Colors
- **Primary Teal**: `#0891A5` (buttons, links, headers)
- **Magenta Accent**: `#C2185B` (CTAs, highlights)
- **Background**: `#F5F5F5` (light gray)
- **White**: `#FFFFFF` (cards, containers)

### Typography
- **Font**: Inter, Segoe UI, system-ui
- **Headings**: Bold, various sizes
- **Body**: Regular, 16px base

## 🔧 Key Routes

- `/` - Homepage
- `/tests` - Test listing with filters
- `/test/<slug>` - Test details
- `/packages` - Package listing
- `/package/<slug>` - Package details
- `/cart` - Shopping cart
- `/booking` - Booking form
- `/confirmation/<booking_number>` - Booking confirmation

## 📱 API Endpoints

- `GET /api/tests` - Get tests with filters (JSON)
- `GET /api/packages` - Get packages (JSON)
- `GET /api/locations` - Get locations (JSON)
- `GET /api/search?q=<query>` - Search tests/packages (JSON)
- `POST /cart/add` - Add item to cart
- `POST /cart/remove` - Remove item from cart
- `POST /booking/submit` - Submit booking

## 🧪 Sample Data

The seed script includes:

**Tests:**
- Lipid Profile
- Complete Blood Count (CBC)
- Thyroid Profile Total
- Liver Function Test (LFT)
- Kidney Function Test (KFT)
- HbA1c (Glycated Hemoglobin)
- Vitamin D (25-OH)
- Vitamin B12

**Packages:**
- Xpert Health Basic (70+ tests)
- Full Body Checkup (95+ tests)
- Diabetes Screening Package
- Heart Health Package

## 🚀 Usage

1. **Browse Tests**: Navigate to "Book A Test" to see all available tests
2. **Filter by Category**: Use the sidebar to filter tests by health conditions
3. **View Details**: Click on any test/package to see detailed information
4. **Add to Cart**: Click "Add to Cart" to add items
5. **Checkout**: Go to cart and proceed to booking
6. **Fill Details**: Enter patient and appointment details
7. **Confirm**: Submit booking and get confirmation

## 🔐 Security Notes

- Change the `SECRET_KEY` in `.env` for production
- Use environment variables for sensitive data
- Implement proper authentication for production use
- Add HTTPS in production

## 📝 Future Enhancements

- User authentication and login
- Payment gateway integration
- Email notifications
- Report upload and viewing
- Admin panel for managing tests and bookings
- SMS notifications
- Doctor consultation booking

## 🤝 Contributing

This is a clone project for educational purposes.

## 📄 License

This project is created for educational purposes.

## 📞 Support

For issues or questions, please check the code comments or Flask documentation.

---

**Built with ❤️ using Flask, MySQL, HTML, CSS, and JavaScript**
