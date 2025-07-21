import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('config.env')

# MongoDB Atlas connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://your_username:your_password@your_cluster.mongodb.net/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'exam_proctoring')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'users')

# Initialize MongoDB client and collection as None
client = None
db = None
collection = None

def initialize_mongodb():
    """Initialize MongoDB connection"""
    global client, db, collection
    
    if client is None:
        try:
            client = MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_NAME]
            # Test connection
            client.admin.command('ping')
            print("✓ MongoDB connection established successfully")
        except Exception as e:
            print(f"✗ MongoDB connection failed: {e}")
            raise e

# Initialize connection when module is imported
initialize_mongodb()

def get_all_details():
    """Get all user details from MongoDB"""
    try:
        if collection is None:
            initialize_mongodb()
        cursor = collection.find({}, {'_id': 0})  # Exclude _id field
        users = list(cursor)
        for user in users:
            print(user)
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

def insert_signup(email, username, password):
    """Insert new user signup data into MongoDB"""
    try:
        if collection is None:
            initialize_mongodb()
            
        # Check if user already exists
        existing_user = collection.find_one({
            '$or': [
                {'email': email},
                {'username': username}
            ]
        })
        
        if existing_user:
            print("User with this email or username already exists!")
            return -1
        
        # Create new user document
        user_data = {
            'email': email,
            'username': username,
            'password': password,
            'created_at': datetime.utcnow()
        }
        
        # Insert the document
        result = collection.insert_one(user_data)
        
        if result.inserted_id:
            print("Sign-Up data credentials inserted successfully!")
            return 1
        else:
            print("Failed to insert user data")
            return -1
            
    except Exception as e:
        print(f"Error inserting user data: {e}")
        return -1

def search_login_credentials(email, password):
    """Search for login credentials in MongoDB"""
    try:
        if collection is None:
            initialize_mongodb()
            
        # Find user with matching email and password
        user = collection.find_one({
            'email': email,
            'password': password
        })
        
        if user:
            print("Data found")
            return True
        else:
            print("No data found.")
            return False
            
    except Exception as e:
        print(f"Error searching login credentials: {e}")
        return False

def get_user_by_email(email):
    """Get user details by email"""
    try:
        if collection is None:
            initialize_mongodb()
        user = collection.find_one({'email': email}, {'_id': 0})
        return user
    except Exception as e:
        print(f"Error fetching user by email: {e}")
        return None

def update_user_password(email, new_password):
    """Update user password"""
    try:
        if collection is None:
            initialize_mongodb()
            
        result = collection.update_one(
            {'email': email},
            {'$set': {'password': new_password}}
        )
        
        if result.modified_count > 0:
            print("Password updated successfully!")
            return True
        else:
            print("No user found with this email")
            return False
            
    except Exception as e:
        print(f"Error updating password: {e}")
        return False

def delete_user(email):
    """Delete user by email"""
    try:
        if collection is None:
            initialize_mongodb()
            
        result = collection.delete_one({'email': email})
        
        if result.deleted_count > 0:
            print("User deleted successfully!")
            return True
        else:
            print("No user found with this email")
            return False
            
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False

if __name__ == "__main__":
    print("Testing MongoDB connection...")
    print(get_all_details())
    # Test insert
    # print(insert_signup('test@example.com', 'testuser', 'testpass'))
    # Test search
    # print(search_login_credentials('test@example.com', 'testpass')) 