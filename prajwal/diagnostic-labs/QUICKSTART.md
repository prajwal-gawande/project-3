# Quick Start Guide - Mom Labs 

## Step-by-Step Instructions

### 1. Navigate to Project Directory
```powershell
cd C:\Users\ratho\Desktop\prajwal\apollo-diagnostics-clone
```

### 2. Install Dependencies (if not done)
```powershell
pip install -r requirements.txt
```

### 3. Test Database Connection
```powershell
python test_db_connection.py
```
**Expected Output:**
```
✅ Database connection successful!
✅ Database 'testdb' created/verified!
```

If you see errors, make sure:
- MySQL is running
- Username: root
- Password: Virendra@30

### 4. Seed the Database
```powershell
python seed_data.py
```
**Expected Output:**
```
Dropping all tables...
Creating all tables...
Creating categories...
Creating tests...
Creating packages...
Creating locations...

✅ Database seeded successfully!
   - 8 categories created
   - 8 tests created
   - 4 packages created
   - 5 locations created
```

### 5. Run the Application
```powershell
python app.py
```
**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 6. Open in Browser
Navigate to: **http://localhost:5000**

---

## Troubleshooting

### If seed_data.py fails:
1. Check MySQL is running: `mysql -u root -pVirendra@30`
2. Manually create database: `CREATE DATABASE testdb;`
3. Run seed_data.py again

### If app.py fails:
1. Check all dependencies installed: `pip list`
2. Check .env file exists with correct credentials
3. Check database was seeded successfully

### If imports fail:
```powershell
pip install Flask Flask-SQLAlchemy PyMySQL python-dotenv
```

---

## Quick Commands Reference

```powershell
# Navigate to project
cd C:\Users\ratho\Desktop\prajwal\apollo-diagnostics-clone

# Install everything
pip install -r requirements.txt

# Setup database
python test_db_connection.py
python seed_data.py

# Run app
python app.py
```

Then open: http://localhost:5000

---

## What You'll See

1. **Homepage** - Featured packages and popular tests
2. **Book A Test** - Browse all diagnostic tests
3. **Test Details** - View test information and pricing
4. **Add to Cart** - Add tests/packages to cart
5. **Cart** - Review your selections
6. **Booking** - Fill patient details and schedule
7. **Confirmation** - Get booking confirmation with ID

---

## Project Features

✅ 8 Diagnostic Tests (Lipid Profile, CBC, Thyroid, etc.)
✅ 4 Health Packages (Full Body Checkup, etc.)
✅ Shopping Cart System
✅ Complete Booking Flow
✅ MySQL Database with SQLAlchemy ORM
✅ Responsive Design
✅ Modern UI (Teal & Magenta Theme)

---

**Need Help?**
Check README.md for detailed documentation!
