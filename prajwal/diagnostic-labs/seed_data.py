from app import app, db
from models import Category, Test, Package, Location
import json


def seed_database():
    """Populate database with initial data"""
    
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        # Create categories
        print("Creating categories...")
        categories_data = [
            {'name': 'Heart', 'slug': 'heart', 'icon': 'heart'},
            {'name': 'Thyroid', 'slug': 'thyroid', 'icon': 'thyroid'},
            {'name': 'Liver', 'slug': 'liver', 'icon': 'liver'},
            {'name': 'Lungs', 'slug': 'lungs', 'icon': 'lungs'},
            {'name': 'Infertility', 'slug': 'infertility', 'icon': 'infertility'},
            {'name': 'Kidney', 'slug': 'kidney', 'icon': 'kidney'},
            {'name': 'Diabetes', 'slug': 'diabetes', 'icon': 'diabetes'},
            {'name': 'Bone Health', 'slug': 'bone-health', 'icon': 'bone'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
            categories[cat_data['slug']] = category
        
        db.session.commit()
        
        # Create tests
        print("Creating tests...")
        tests_data = [
            {
                'name': 'LIPID PROFILE',
                'slug': 'lipid-profile',
                'description': 'A lipid profile test is a crucial diagnostic tool used to assess the levels of various types of fats, or lipids, in your blood. This test provides a comprehensive evaluation of your cardiovascular health by measuring several key components: total cholesterol, low-density lipoprotein (LDL) cholesterol, high-density lipoprotein (HDL) cholesterol, very-low-density lipoprotein (VLDL) cholesterol, and triglycerides. Each of these lipids plays a distinct role in your body\'s metabolic processes and has implications for your heart health.',
                'price': 800,
                'original_price': 1067,
                'discount': 25,
                'sample_type': 'Blood',
                'report_delivery': 'Same Day',
                'home_collection': True,
                'preparation': 'Fasting for atleast 12 hours before the test is mandatory.',
                'parameters': ['Total Cholesterol', 'LDL Cholesterol', 'HDL Cholesterol', 'Triglycerides', 'VLDL Cholesterol'],
                'test_count': 5,
                'category': categories['heart']
            },
            {
                'name': 'COMPLETE BLOOD COUNT (CBC)',
                'slug': 'complete-blood-count-cbc',
                'description': 'A Complete Blood Count (CBC) is one of the most common blood tests and provides important information about the types and numbers of cells in your blood. It helps diagnose a wide range of conditions including anemia, infection, and many other disorders.',
                'price': 350,
                'original_price': 500,
                'discount': 30,
                'sample_type': 'Blood',
                'report_delivery': 'Same Day',
                'home_collection': True,
                'preparation': 'No special preparation required.',
                'parameters': ['Hemoglobin', 'RBC Count', 'WBC Count', 'Platelet Count', 'Hematocrit', 'MCV', 'MCH', 'MCHC'],
                'test_count': 8,
                'category': categories['heart']
            },
            {
                'name': 'THYROID PROFILE TOTAL',
                'slug': 'thyroid-profile-total',
                'description': 'The Thyroid Profile Total test measures the levels of thyroid hormones in your blood. The thyroid gland produces hormones that regulate metabolism, energy levels, and overall growth and development.',
                'price': 600,
                'original_price': 800,
                'discount': 25,
                'sample_type': 'Blood',
                'report_delivery': '1 DAY',
                'home_collection': True,
                'preparation': 'No special preparation required.',
                'parameters': ['T3 Total', 'T4 Total', 'TSH'],
                'test_count': 3,
                'category': categories['thyroid']
            },
            {
                'name': 'LIVER FUNCTION TEST (LFT)',
                'slug': 'liver-function-test-lft',
                'description': 'Liver Function Test (LFT) is a group of blood tests that provide information about the state of a patient\'s liver. These tests measure various enzymes, proteins, and substances that are produced or processed by the liver.',
                'price': 550,
                'original_price': 750,
                'discount': 27,
                'sample_type': 'Blood',
                'report_delivery': 'Same Day',
                'home_collection': True,
                'preparation': 'Fasting for 8-12 hours is recommended.',
                'parameters': ['Bilirubin Total', 'Bilirubin Direct', 'SGOT', 'SGPT', 'Alkaline Phosphatase', 'Total Protein', 'Albumin', 'Globulin'],
                'test_count': 8,
                'category': categories['liver']
            },
            {
                'name': 'KIDNEY FUNCTION TEST (KFT)',
                'slug': 'kidney-function-test-kft',
                'description': 'Kidney Function Test (KFT) is a comprehensive metabolic panel that measures how well your kidneys are working. It checks the levels of various substances in your blood that are filtered by the kidneys.',
                'price': 500,
                'original_price': 650,
                'discount': 23,
                'sample_type': 'Blood',
                'report_delivery': 'Same Day',
                'home_collection': True,
                'preparation': 'No special preparation required.',
                'parameters': ['Urea', 'Creatinine', 'Uric Acid', 'BUN', 'Sodium', 'Potassium', 'Chloride'],
                'test_count': 7,
                'category': categories['kidney']
            },
            {
                'name': 'HbA1c (GLYCATED HEMOGLOBIN)',
                'slug': 'hba1c-glycated-hemoglobin',
                'description': 'The HbA1c test measures your average blood sugar levels over the past 2-3 months. It is a key test for diagnosing and monitoring diabetes.',
                'price': 450,
                'original_price': 600,
                'discount': 25,
                'sample_type': 'Blood',
                'report_delivery': 'Same Day',
                'home_collection': True,
                'preparation': 'No fasting required.',
                'parameters': ['HbA1c'],
                'test_count': 1,
                'category': categories['diabetes']
            },
            {
                'name': 'VITAMIN D (25-OH)',
                'slug': 'vitamin-d-25-oh',
                'description': 'Vitamin D test measures the level of vitamin D in your blood. Vitamin D is essential for bone health, immune function, and overall well-being.',
                'price': 900,
                'original_price': 1200,
                'discount': 25,
                'sample_type': 'Blood',
                'report_delivery': '2 DAYS',
                'home_collection': True,
                'preparation': 'No special preparation required.',
                'parameters': ['Vitamin D (25-OH)'],
                'test_count': 1,
                'category': categories['bone-health']
            },
            {
                'name': 'VITAMIN B12',
                'slug': 'vitamin-b12',
                'description': 'Vitamin B12 test measures the amount of vitamin B12 in your blood. This vitamin is important for brain function, nerve tissue health, and the production of red blood cells.',
                'price': 750,
                'original_price': 1000,
                'discount': 25,
                'sample_type': 'Blood',
                'report_delivery': '2 DAYS',
                'home_collection': True,
                'preparation': 'No special preparation required.',
                'parameters': ['Vitamin B12'],
                'test_count': 1,
                'category': categories['heart']
            }
        ]
        
        tests = {}
        for test_data in tests_data:
            # Extract parameters and category
            params = test_data.pop('parameters')
            category = test_data.pop('category')
            
            # Create test
            test = Test(**test_data, category=category)
            test.parameters = params  # Use the property setter
            db.session.add(test)
            tests[test_data['slug']] = test
        
        db.session.commit()
        
        # Create packages
        print("Creating packages...")
        packages_data = [
            {
                'name': 'Xpert Health Basic',
                'slug': 'xpert-health-basic',
                'description': 'Comprehensive health checkup package covering 70+ essential tests for overall health assessment.',
                'price': 1699,
                'original_price': 2265,
                'discount': 25,
                'test_count': 70,
                'legacy': '40+ Yrs of Legacy',
                'home_collection': True,
                'is_featured': True,
                'test_slugs': ['lipid-profile', 'complete-blood-count-cbc', 'thyroid-profile-total', 'liver-function-test-lft', 'kidney-function-test-kft', 'hba1c-glycated-hemoglobin']
            },
            {
                'name': 'Full Body Checkup',
                'slug': 'full-body-checkup',
                'description': 'Complete body checkup with all essential tests for comprehensive health evaluation.',
                'price': 2499,
                'original_price': 3500,
                'discount': 29,
                'test_count': 95,
                'legacy': '40+ Yrs of Legacy',
                'home_collection': True,
                'is_featured': True,
                'test_slugs': ['lipid-profile', 'complete-blood-count-cbc', 'thyroid-profile-total', 'liver-function-test-lft', 'kidney-function-test-kft', 'hba1c-glycated-hemoglobin', 'vitamin-d-25-oh', 'vitamin-b12']
            },
            {
                'name': 'Diabetes Screening Package',
                'slug': 'diabetes-screening-package',
                'description': 'Specialized package for diabetes screening and monitoring.',
                'price': 899,
                'original_price': 1200,
                'discount': 25,
                'test_count': 15,
                'legacy': '40+ Yrs of Legacy',
                'home_collection': True,
                'is_featured': False,
                'test_slugs': ['hba1c-glycated-hemoglobin', 'lipid-profile', 'kidney-function-test-kft']
            },
            {
                'name': 'Heart Health Package',
                'slug': 'heart-health-package',
                'description': 'Comprehensive cardiac health assessment package.',
                'price': 1299,
                'original_price': 1800,
                'discount': 28,
                'test_count': 25,
                'legacy': '40+ Yrs of Legacy',
                'home_collection': True,
                'is_featured': True,
                'test_slugs': ['lipid-profile', 'complete-blood-count-cbc', 'hba1c-glycated-hemoglobin']
            }
        ]
        
        for pkg_data in packages_data:
            # Extract test slugs
            test_slugs = pkg_data.pop('test_slugs')
            
            # Create package
            package = Package(**pkg_data)
            
            # Add tests to package
            for slug in test_slugs:
                if slug in tests:
                    package.tests.append(tests[slug])
            
            db.session.add(package)
        
        db.session.commit()
        
        # Create locations
        print("Creating locations...")
        locations_data = [
            {
                'city': 'Hyderabad',
                'state': 'Telangana',
                'address': 'Apollo Diagnostics, Banjara Hills, Road No. 12',
                'pincode': '500034',
                'phone': '040-4444-2424',
                'latitude': 17.4239,
                'longitude': 78.4738
            },
            {
                'city': 'Hyderabad',
                'state': 'Telangana',
                'address': 'Apollo Diagnostics, Jubilee Hills, Road No. 36',
                'pincode': '500033',
                'phone': '040-4444-2424',
                'latitude': 17.4326,
                'longitude': 78.4071
            },
            {
                'city': 'Hyderabad',
                'state': 'Telangana',
                'address': 'Apollo Diagnostics, Kukatpally, KPHB Colony',
                'pincode': '500072',
                'phone': '040-4444-2424',
                'latitude': 17.4849,
                'longitude': 78.3866
            },
            {
                'city': 'Bangalore',
                'state': 'Karnataka',
                'address': 'Apollo Diagnostics, Koramangala, 5th Block',
                'pincode': '560095',
                'phone': '080-4444-2424',
                'latitude': 12.9352,
                'longitude': 77.6245
            },
            {
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Apollo Diagnostics, Andheri West, Lokhandwala',
                'pincode': '400053',
                'phone': '022-4444-2424',
                'latitude': 19.1368,
                'longitude': 72.8340
            }
        ]
        
        for loc_data in locations_data:
            location = Location(**loc_data)
            db.session.add(location)
        
        db.session.commit()
        
        print("\n✅ Database seeded successfully!")
        print(f"   - {len(categories_data)} categories created")
        print(f"   - {len(tests_data)} tests created")
        print(f"   - {len(packages_data)} packages created")
        print(f"   - {len(locations_data)} locations created")


if __name__ == '__main__':
    seed_database()
