import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Testing bcrypt authentication fix...")
print("-" * 50)

# Test 1: Check if monkey-patch works
print("\n1. Testing bcrypt import and monkey-patch...")
import bcrypt
if hasattr(bcrypt, '__about__'):
    print(f"   ✅ bcrypt.__about__ exists")
    print(f"   ✅ Version: {bcrypt.__about__.__version__}")
else:
    print(f"   ❌ bcrypt.__about__ does NOT exist - patch failed!")

# Test 2: Test passlib import
print("\n2. Testing passlib import...")
try:
    from passlib.context import CryptContext
    print("   ✅ passlib imported successfully")
except Exception as e:
    print(f"   ❌ passlib import failed: {e}")

# Test 3: Test password hashing and verification
print("\n3. Testing password hash and verify...")
try:
    from repositories.user_repository import UserRepository
    
    # Hash a password
    test_password = "password"
    hashed = UserRepository.get_password_hash(test_password)
    print(f"   ✅ Password hashed successfully")
    print(f"   Hash: {hashed[:50]}...")
    
    # Verify the password
    is_valid = UserRepository.verify_password(test_password, hashed)
    if is_valid:
        print(f"   ✅ Password verification works!")
    else:
        print(f"   ❌ Password verification FAILED")
    
    # Test wrong password
    is_invalid = UserRepository.verify_password("wrong_password", hashed)
    if not is_invalid:
        print(f"   ✅ Wrong password correctly rejected")
    else:
        print(f"   ❌ Wrong password was accepted (BUG!)")
        
except Exception as e:
    print(f"   ❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Test actual user authentication
print("\n4. Testing user authentication from database...")
try:
    from database.database import SessionLocal
    
    db = SessionLocal()
    user = UserRepository.authenticate(db, "teacher1", "password")
    
    if user:
        print(f"   ✅ Authentication SUCCESS!")
        print(f"   User: {user.username} ({user.full_name})")
        print(f"   Role: {user.role}")
    else:
        print(f"   ❌ Authentication FAILED - user not found or password incorrect")
    
    db.close()
    
except Exception as e:
    print(f"   ❌ Authentication test error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test completed!")
