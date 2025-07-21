#!/usr/bin/env python3
"""
Migration Script: MySQL to MongoDB Atlas

This script helps migrate existing MySQL data to MongoDB Atlas
for the AI-Based Online Exam Proctoring System.
"""

import mysql.connector
import pymongo
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

def connect_mysql():
    """Connect to MySQL database"""
    try:
        # MySQL connection (old database)
        mysql_connection = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="root", 
            database="quizo"
        )
        print("✓ Connected to MySQL database")
        return mysql_connection
    except mysql.connector.Error as err:
        print(f"✗ MySQL connection failed: {err}")
        return None

def connect_mongodb():
    """Connect to MongoDB Atlas"""
    try:
        # Load environment variables
        load_dotenv('config.env')
        
        # MongoDB Atlas connection
        mongo_uri = os.getenv('MONGO_URI')
        database_name = os.getenv('DATABASE_NAME', 'exam_proctoring')
        collection_name = os.getenv('COLLECTION_NAME', 'users')
        
        if not mongo_uri:
            print("✗ MONGO_URI not found in config.env")
            return None, None, None
        
        client = pymongo.MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        
        # Test connection
        client.admin.command('ping')
        print("✓ Connected to MongoDB Atlas")
        return client, db, collection
        
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return None, None, None

def migrate_users(mysql_connection, mongo_collection):
    """Migrate user data from MySQL to MongoDB"""
    try:
        # Get users from MySQL
        cursor = mysql_connection.cursor()
        cursor.execute("SELECT email, username, password FROM quizo.sign_up")
        mysql_users = cursor.fetchall()
        cursor.close()
        
        print(f"Found {len(mysql_users)} users in MySQL database")
        
        migrated_count = 0
        skipped_count = 0
        
        for user in mysql_users:
            email, username, password = user
            
            # Check if user already exists in MongoDB
            existing_user = mongo_collection.find_one({
                '$or': [
                    {'email': email},
                    {'username': username}
                ]
            })
            
            if existing_user:
                print(f"⚠ User {email} already exists in MongoDB, skipping...")
                skipped_count += 1
                continue
            
            # Create user document for MongoDB
            user_doc = {
                'email': email,
                'username': username,
                'password': password,
                'created_at': datetime.utcnow(),
                'migrated_from_mysql': True,
                'migration_date': datetime.utcnow()
            }
            
            # Insert into MongoDB
            result = mongo_collection.insert_one(user_doc)
            
            if result.inserted_id:
                print(f"✓ Migrated user: {email}")
                migrated_count += 1
            else:
                print(f"✗ Failed to migrate user: {email}")
        
        print(f"\nMigration Summary:")
        print(f"  - Successfully migrated: {migrated_count} users")
        print(f"  - Skipped (already exists): {skipped_count} users")
        print(f"  - Total processed: {len(mysql_users)} users")
        
        return migrated_count
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return 0

def verify_migration(mongo_collection):
    """Verify the migration by checking data integrity"""
    print("\nVerifying migration...")
    
    try:
        # Count total users
        total_users = mongo_collection.count_documents({})
        migrated_users = mongo_collection.count_documents({'migrated_from_mysql': True})
        
        print(f"✓ Total users in MongoDB: {total_users}")
        print(f"✓ Migrated users: {migrated_users}")
        
        # Show sample migrated users
        sample_users = mongo_collection.find({'migrated_from_mysql': True}).limit(3)
        print("\nSample migrated users:")
        for user in sample_users:
            print(f"  - {user['email']} ({user['username']})")
        
        return True
        
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False

def cleanup_mysql_connection(mysql_connection):
    """Close MySQL connection"""
    if mysql_connection:
        mysql_connection.close()
        print("✓ MySQL connection closed")

def main():
    """Main migration function"""
    print("=" * 60)
    print("MySQL to MongoDB Atlas Migration Tool")
    print("=" * 60)
    
    # Connect to MySQL
    mysql_connection = connect_mysql()
    if not mysql_connection:
        print("Cannot proceed without MySQL connection")
        sys.exit(1)
    
    # Connect to MongoDB
    mongo_client, mongo_db, mongo_collection = connect_mongodb()
    if not mongo_collection:
        print("Cannot proceed without MongoDB connection")
        cleanup_mysql_connection(mysql_connection)
        sys.exit(1)
    
    try:
        # Perform migration
        migrated_count = migrate_users(mysql_connection, mongo_collection)
        
        if migrated_count > 0:
            # Verify migration
            verify_migration(mongo_collection)
            
            print("\n" + "=" * 60)
            print("Migration completed successfully!")
            print("You can now use the MongoDB Atlas version of the application.")
            print("=" * 60)
        else:
            print("\nNo users were migrated. Check the logs above for details.")
            
    except KeyboardInterrupt:
        print("\nMigration interrupted by user")
    except Exception as e:
        print(f"\nMigration failed with error: {e}")
    finally:
        # Cleanup
        cleanup_mysql_connection(mysql_connection)
        if mongo_client:
            mongo_client.close()
            print("✓ MongoDB connection closed")

if __name__ == "__main__":
    main() 