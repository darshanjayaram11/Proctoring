#!/usr/bin/env python3
"""
Test MongoDB Connection Script

This script tests the MongoDB Atlas connection with the provided credentials.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    print("Testing MongoDB Atlas connection...")
    
    # Load environment variables
    load_dotenv('config.env')
    
    # Get connection string
    mongo_uri = os.getenv('MONGO_URI')
    database_name = os.getenv('DATABASE_NAME', 'exam_proctoring')
    collection_name = os.getenv('COLLECTION_NAME', 'users')
    
    print(f"Connection string: {mongo_uri}")
    print(f"Database: {database_name}")
    print(f"Collection: {collection_name}")
    
    try:
        # Create MongoDB client
        client = MongoClient(mongo_uri)
        
        # Test connection
        client.admin.command('ping')
        print("✓ MongoDB connection successful!")
        
        # Test database access
        db = client[database_name]
        collection = db[collection_name]
        
        # Test collection operations
        count = collection.count_documents({})
        print(f"✓ Collection accessible. Document count: {count}")
        
        # Test insert operation
        test_doc = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass',
            'test': True
        }
        
        result = collection.insert_one(test_doc)
        print(f"✓ Insert test successful. ID: {result.inserted_id}")
        
        # Clean up test document
        collection.delete_one({'_id': result.inserted_id})
        print("✓ Cleanup successful")
        
        client.close()
        print("✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_mongodb_connection() 