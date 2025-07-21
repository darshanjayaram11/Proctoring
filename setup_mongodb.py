#!/usr/bin/env python3
"""
MongoDB Atlas Setup Script for AI-Based Online Exam Proctoring System

This script helps initialize the MongoDB Atlas database with sample data
and validates the connection.
"""

import os
import sys
from dotenv import load_dotenv
from backend.mongo_helper import *

def setup_database():
    """Initialize the database with sample data"""
    print("Setting up MongoDB Atlas database...")
    
    # Test connection
    try:
        # Test basic connection
        users = get_all_details()
        print("✓ Database connection successful!")
        
        # Check if sample data exists
        if not users:
            print("No users found. Adding sample data...")
            add_sample_data()
        else:
            print(f"Found {len(users)} existing users in database.")
            
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease check your MongoDB Atlas configuration:")
        print("1. Verify your connection string in config.env")
        print("2. Ensure your IP is whitelisted in MongoDB Atlas")
        print("3. Check username and password")
        return False
    
    return True

def add_sample_data():
    """Add sample user data to the database"""
    sample_users = [
        {
            'email': 'admin@examportal.com',
            'username': 'ExamPortalAdmin',
            'password': 'Admin@123'
        },
        {
            'email': 'student1@example.com',
            'username': 'student1',
            'password': 'Student@123'
        },
        {
            'email': 'student2@example.com',
            'username': 'student2',
            'password': 'Student@123'
        },
        {
            'email': 'teacher@example.com',
            'username': 'teacher',
            'password': 'Teacher@123'
        }
    ]
    
    for user in sample_users:
        result = insert_signup(user['email'], user['username'], user['password'])
        if result == 1:
            print(f"✓ Added user: {user['email']}")
        else:
            print(f"✗ Failed to add user: {user['email']}")

def test_authentication():
    """Test authentication functionality"""
    print("\nTesting authentication...")
    
    # Test login with sample credentials
    test_email = 'admin@examportal.com'
    test_password = 'Admin@123'
    
    result = search_login_credentials(test_email, test_password)
    if result:
        print("✓ Authentication test successful!")
    else:
        print("✗ Authentication test failed!")

def validate_environment():
    """Validate environment configuration"""
    print("Validating environment configuration...")
    
    # Load environment variables
    load_dotenv('config.env')
    
    required_vars = ['MONGO_URI', 'DATABASE_NAME', 'COLLECTION_NAME']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"✗ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your config.env file.")
        return False
    else:
        print("✓ All required environment variables are set.")
        return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("AI-Based Online Exam Proctoring System - MongoDB Setup")
    print("=" * 60)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    # Test authentication
    test_authentication()
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("You can now run the application with: python server.py")
    print("=" * 60)

if __name__ == "__main__":
    main() 