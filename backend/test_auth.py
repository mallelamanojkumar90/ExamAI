from main import get_password_hash, verify_password

def test_auth_flow():
    password = "password123"
    print(f"Testing with password: {password}")
    
    # 1. Hash
    hashed = get_password_hash(password)
    print(f"Hashed (str): {hashed}")
    print(f"Hashed type: {type(hashed)}")
    
    # 2. Verify
    result = verify_password(password, hashed)
    print(f"Verification result: {result}")
    
    if result:
        print("SUCCESS: Password verified.")
    else:
        print("FAILURE: Password verification failed.")

if __name__ == "__main__":
    test_auth_flow()
