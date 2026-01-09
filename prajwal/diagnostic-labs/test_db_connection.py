import pymysql

try:
    # Test database connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Virendra@30',  # Direct password, no URL encoding needed
        charset='utf8mb4'
    )
    print("✅ Database connection successful!")
    
    # Create database if it doesn't exist
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✅ Database 'testdb' created/verified!")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("\nPlease check:")
    print("1. MySQL server is running")
    print("2. Username is 'root'")
    print("3. Password is 'Virendra@30'")
    print("4. MySQL is accessible on localhost")
