import subprocess
import sys
import os

# Auto-install required packages
def install_packages():
    """Automatically install required packages"""
    required_packages = ['bit', 'ecdsa']
    
    print("="*60)
    print("Checking and installing required packages...")
    print("="*60)
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print(f"✓ {package} installed successfully")
    print()

# Install packages before importing
install_packages()

import random
import time
from datetime import datetime
from bit import Key

# ==================== PUZZLE #73 PARAMETERS ====================
TARGET_ADDRESS = "12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4"
START_HEX = "1000000000000000000"
END_HEX = "1ffffffffffffffffff"
# ===============================================================

# Convert hex strings to integers
start_range = int(START_HEX, 16)
end_range = int(END_HEX, 16)

print("="*70)
print(" "*20 + "BTC PUZZLE #73 SOLVER")
print(" "*20 + "Random Search Method")
print("="*70)
print(f"Target Address  : {TARGET_ADDRESS}")
print(f"Start Range (HEX): 0x{START_HEX}")
print(f"End Range (HEX)  : 0x{END_HEX}")
print(f"Search Space     : {end_range - start_range + 1:,} possible keys")
print(f"Bits             : 73")
print("="*70)

def private_key_to_address(private_key_int):
    """Convert private key integer to Bitcoin address"""
    try:
        # Convert to hex and pad to 64 characters
        private_key_hex = hex(private_key_int)[2:].zfill(64)
        # Generate Bitcoin key
        key = Key.from_hex(private_key_hex)
        return key.address, private_key_hex
    except Exception as e:
        return None, None

def save_result(private_key_hex, private_key_dec, address, attempts, elapsed):
    """Save the found key to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "PUZZLE_73_SOLVED.txt"
    
    with open(filename, "w") as f:
        f.write("="*70 + "\n")
        f.write(" "*25 + "PUZZLE #73 SOLVED!\n")
        f.write("="*70 + "\n\n")
        f.write(f"Timestamp       : {timestamp}\n")
        f.write(f"Target Address  : {TARGET_ADDRESS}\n")
        f.write(f"Found Address   : {address}\n\n")
        f.write(f"Private Key (HEX): {private_key_hex}\n")
        f.write(f"Private Key (DEC): {private_key_dec}\n\n")
        f.write(f"Total Attempts  : {attempts:,}\n")
        f.write(f"Time Elapsed    : {elapsed:.2f} seconds\n")
        f.write(f"Speed           : {attempts/elapsed:.2f} keys/sec\n")
        f.write("="*70 + "\n")
    
    print(f"\n✓ Results saved to: {filename}")

def main():
    """Main search function"""
    attempts = 0
    start_time = time.time()
    last_update = start_time
    
    print("\nStarting random search...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Generate random private key in range
            random_key = random.randint(start_range, end_range)
            
            # Convert to address
            address, private_key_hex = private_key_to_address(random_key)
            
            if address is None:
                continue
            
            attempts += 1
            
            # Update progress every 1000 attempts
            current_time = time.time()
            if attempts % 1000 == 0:
                elapsed = current_time - start_time
                speed = attempts / elapsed if elapsed > 0 else 0
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"Attempts: {attempts:,} | "
                      f"Speed: {speed:.2f} keys/s | "
                      f"Current: 0x{private_key_hex[:16]}...")
            
            # Check if we found the target address
            if address == TARGET_ADDRESS:
                elapsed = current_time - start_time
                
                print("\n" + "="*70)
                print(" "*25 + "🎉 PUZZLE SOLVED! 🎉")
                print("="*70)
                print(f"\nPrivate Key (HEX): {private_key_hex}")
                print(f"Private Key (DEC): {random_key}")
                print(f"Address          : {address}")
                print(f"\nTotal Attempts   : {attempts:,}")
                print(f"Time Elapsed     : {elapsed:.2f} seconds")
                print(f"Speed            : {attempts/elapsed:.2f} keys/sec")
                print("="*70)
                
                save_result(private_key_hex, random_key, address, attempts, elapsed)
                break
                
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        
        print("\n\n" + "="*70)
        print(" "*25 + "SEARCH STOPPED")
        print("="*70)
        print(f"Total Attempts: {attempts:,}")
        print(f"Time Elapsed  : {elapsed:.2f} seconds")
        if elapsed > 0:
            print(f"Average Speed : {attempts/elapsed:.2f} keys/sec")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
