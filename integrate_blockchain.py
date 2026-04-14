#!/usr/bin/env python3
"""
Blockchain Integration Script
Helps you set up blockchain integration for SecureCloud
"""

import os
import sys
from pathlib import Path

def check_web3():
    """Check if web3 is installed"""
    try:
        import web3
        print("[OK] web3 library is installed")
        return True
    except ImportError:
        print("[WARNING] web3 library is not installed")
        print("\nTo install web3:")
        print("  pip install web3==6.20.1")
        print("\nNote: On Windows, you may need Visual C++ Build Tools")
        print("Download from: https://visualstudio.microsoft.com/downloads/")
        return False

def check_env_file():
    """Check if .env.mysql exists"""
    env_file = Path('.env.mysql')
    if env_file.exists():
        print("[OK] .env.mysql file found")
        return True
    else:
        print("[ERROR] .env.mysql file not found")
        print("Create it by copying from .env.mysql.example or create it manually")
        return False

def read_env_file():
    """Read current .env.mysql file"""
    env_file = Path('.env.mysql')
    if not env_file.exists():
        return {}
    
    env_vars = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def check_blockchain_config():
    """Check blockchain configuration"""
    env_vars = read_env_file()
    
    required = {
        'BLOCKCHAIN_RPC_URL': 'Infura RPC URL',
        'BLOCKCHAIN_CONTRACT_ADDRESS': 'Smart contract address',
        'BLOCKCHAIN_PRIVATE_KEY': 'Ethereum wallet private key',
        'BLOCKCHAIN_CHAIN_ID': 'Network chain ID (11155111 for Sepolia)'
    }
    
    print("\n" + "="*60)
    print("Blockchain Configuration Status")
    print("="*60)
    
    all_set = True
    for var, desc in required.items():
        value = env_vars.get(var, '')
        if value:
            # Mask sensitive values
            if 'PRIVATE_KEY' in var:
                display = value[:10] + "..." + value[-8:] if len(value) > 18 else "***"
            else:
                display = value
            print(f"[OK] {var}: {display}")
        else:
            print(f"[MISSING] {var}: {desc}")
            all_set = False
    
    print("="*60)
    return all_set, env_vars

def generate_wallet():
    """Generate a new Ethereum wallet"""
    try:
        from eth_account import Account
        import secrets
        
        print("\nGenerating new Ethereum wallet...")
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        account = Account.from_key(private_key)
        
        print("\n" + "="*60)
        print("NEW WALLET GENERATED")
        print("="*60)
        print(f"Address:     {account.address}")
        print(f"Private Key: {private_key}")
        print("="*60)
        print("\nIMPORTANT:")
        print("1. Save this private key securely")
        print("2. Never share it or commit to Git")
        print("3. Get testnet ETH from: https://sepoliafaucet.com/")
        print("4. Add it to your .env.mysql file")
        print("="*60)
        
        return account.address, private_key
    except ImportError:
        print("[ERROR] eth_account not available")
        print("Install with: pip install eth-account")
        return None, None

def update_env_file(env_vars):
    """Update .env.mysql with blockchain config"""
    env_file = Path('.env.mysql')
    
    # Read existing content
    lines = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            lines = f.readlines()
    
    # Check if blockchain section exists
    blockchain_section = False
    blockchain_vars = {
        'BLOCKCHAIN_RPC_URL': '',
        'BLOCKCHAIN_CONTRACT_ADDRESS': '0xd9145CCE52D386f254917e481eB44e9943F39138',
        'BLOCKCHAIN_PRIVATE_KEY': '',
        'BLOCKCHAIN_CHAIN_ID': '11155111'
    }
    
    # Update existing values or add new ones
    new_lines = []
    blockchain_added = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# Blockchain'):
            blockchain_section = True
            new_lines.append(line)
        elif blockchain_section and any(var in line for var in blockchain_vars.keys()):
            # Update existing blockchain var
            key = line.split('=')[0].strip()
            if key in env_vars and env_vars[key]:
                new_lines.append(f"{key}={env_vars[key]}\n")
            else:
                new_lines.append(line)
        elif blockchain_section and stripped and not stripped.startswith('#'):
            # End of blockchain section
            blockchain_section = False
            new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Add blockchain section if not present
    if not any('BLOCKCHAIN' in line for line in new_lines):
        new_lines.append("\n# Blockchain Configuration\n")
        for key, default in blockchain_vars.items():
            value = env_vars.get(key, default) if key != 'BLOCKCHAIN_PRIVATE_KEY' else env_vars.get(key, '')
            if value:
                new_lines.append(f"{key}={value}\n")
        new_lines.append("\n")
    
    # Write back
    with open(env_file, 'w') as f:
        f.writelines(new_lines)
    
    print(f"\n[OK] Updated {env_file}")

def test_connection():
    """Test blockchain connection"""
    try:
        from blockchain_logger import is_blockchain_configured, _init_web3
        from blockchain_logger import _web3
        
        _init_web3()
        
        if is_blockchain_configured():
            print("\n[OK] Blockchain is properly configured!")
            
            if _web3 and _web3.is_connected():
                latest_block = _web3.eth.get_block('latest')
                print(f"[OK] Connected to blockchain")
                print(f"   Latest block: {latest_block.number}")
                chain_id = _web3.eth.chain_id
                network = "Sepolia Testnet" if chain_id == 11155111 else f"Network (Chain ID: {chain_id})"
                print(f"   Network: {network}")
                return True
            else:
                print("[ERROR] Cannot connect to blockchain RPC")
                return False
        else:
            print("\n[ERROR] Blockchain is not properly configured")
            print("Check your .env.mysql file")
            return False
    except Exception as e:
        print(f"\n[ERROR] Error testing connection: {e}")
        return False

def main():
    """Main integration function"""
    print("="*60)
    print("SecureCloud Blockchain Integration")
    print("="*60)
    
    # Step 1: Check web3
    print("\n[Step 1] Checking web3 library...")
    web3_installed = check_web3()
    
    if not web3_installed:
        print("\n[ACTION REQUIRED] Install web3 first:")
        print("  pip install web3==6.20.1")
        print("\nIf installation fails on Windows, install Visual C++ Build Tools")
        print("The app will work without blockchain, but blockchain features will be disabled.")
    
    # Step 2: Check env file
    print("\n[Step 2] Checking .env.mysql file...")
    if not check_env_file():
        print("\n[ACTION REQUIRED] Create .env.mysql file first")
        return
    
    # Step 3: Check configuration
    print("\n[Step 3] Checking blockchain configuration...")
    all_set, env_vars = check_blockchain_config()
    
    if not all_set:
        print("\n[MISSING CONFIGURATION]")
        print("\nYou need to configure:")
        print("1. BLOCKCHAIN_RPC_URL - Get from Infura (https://infura.io)")
        print("2. BLOCKCHAIN_CONTRACT_ADDRESS - Use pre-deployed: 0xd9145CCE52D386f254917e481eB44e9943F39138")
        print("3. BLOCKCHAIN_PRIVATE_KEY - Generate wallet or use MetaMask")
        print("4. BLOCKCHAIN_CHAIN_ID - Use 11155111 for Sepolia testnet")
        print("\nSee BLOCKCHAIN_QUICK_START.md for detailed instructions")
        
        # Offer to generate wallet
        if not env_vars.get('BLOCKCHAIN_PRIVATE_KEY'):
            print("\nWould you like to generate a new wallet? (Run with --generate-wallet)")
    
    # Step 4: Test connection
    if all_set and web3_installed:
        print("\n[Step 4] Testing blockchain connection...")
        test_connection()
    
    print("\n" + "="*60)
    print("Integration Check Complete")
    print("="*60)
    
    if all_set and web3_installed:
        print("\n[SUCCESS] Blockchain is ready!")
        print("Restart your Flask app to enable blockchain logging.")
    else:
        print("\n[INCOMPLETE] Complete the setup steps above")
        print("See BLOCKCHAIN_QUICK_START.md for help")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-wallet":
        generate_wallet()
    else:
        main()
