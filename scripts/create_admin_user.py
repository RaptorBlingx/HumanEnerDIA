#!/usr/bin/env python3
"""
Create Admin User Script
Creates an admin user with specified credentials
"""

import bcrypt
import psycopg2
from datetime import datetime
import os
import sys

# Database configuration from environment
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'enms')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')

def hash_password(password: str) -> str:
    """Hash password using bcrypt with 12 rounds"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_admin_user(email: str, password: str, full_name: str = "Admin User", 
                     organization: str = "ENMS", position: str = "Administrator",
                     country: str = "Turkey"):
    """Create or update user as admin"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id, email, role FROM demo_users WHERE email = %s", (email.lower(),))
        existing_user = cursor.fetchone()
        
        password_hash = hash_password(password)
        
        if existing_user:
            # Update existing user to admin
            cursor.execute("""
                UPDATE demo_users 
                SET 
                    password_hash = %s,
                    role = 'admin',
                    email_verified = TRUE,
                    verified_at = NOW(),
                    is_active = TRUE,
                    updated_at = NOW()
                WHERE email = %s
                RETURNING id, email, role
            """, (password_hash, email.lower()))
            
            user = cursor.fetchone()
            conn.commit()
            
            print(f"✅ Updated existing user to admin:")
            print(f"   ID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Role: {user[2]}")
            
        else:
            # Create new admin user
            cursor.execute("""
                INSERT INTO demo_users (
                    email, password_hash, organization, full_name, position, country,
                    role, email_verified, verified_at, is_active, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'admin', TRUE, NOW(), TRUE, NOW())
                RETURNING id, email, role
            """, (
                email.lower(), password_hash, organization, full_name, 
                position, country
            ))
            
            user = cursor.fetchone()
            conn.commit()
            
            print(f"✅ Created new admin user:")
            print(f"   ID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Role: {user[2]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    # Admin credentials
    admin_email = "yazilim.aarti.muhendislik@gmail.com"
    admin_password = "Raptor@321"
    
    print(f"Creating admin user: {admin_email}")
    success = create_admin_user(
        email=admin_email,
        password=admin_password,
        full_name="Aarti Muhendislik Admin",
        organization="Aarti Muhendislik",
        position="System Administrator",
        country="Turkey"
    )
    
    if success:
        print(f"\n✅ Admin user ready!")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print(f"   You can now login at: http://10.33.10.104:8080/login.html")
    else:
        print("\n❌ Failed to create admin user")
        sys.exit(1)
