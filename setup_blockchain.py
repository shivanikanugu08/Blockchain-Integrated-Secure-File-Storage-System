#!/usr/bin/env python3
"""
Blockchain Setup Helper Script
Helps you configure blockchain integration for SecureCloud
"""

import os
import sys
from dotenv import load_dotenv

def check_web3_installed():
    """Check if web3 is installed"""
    try:
        import web3
        print("[OK] web3 is installed")
        return True
    except ImportError:
        print("[ERROR] web3 is not installed")
        print("\nInstall it with: pip install web3==6.20.1")
        return False

def check_env_file():
    """Check if .env.mysql exists"""
    if os.path.exists('.env.mysql'):
        print("[OK] .env.mysql file found")
        return True
    else:
        print("[ERROR] .env.mysql file not found")
        print("\nCreate it by copying from .env.mysql.example")
        return False

def check_blockchain_config():
    """Check blockchain configuration in .env.mysql"""
    load_dotenv('.env.mysql')
    
    required_vars = {
        'BLOCKCHAIN_RPC_URL': os.getenv('BLOCKCHAIN_RPC_URL'),
        'BLOCKCHAIN_CONTRACT_ADDRESS': os.getenv('BLOCKCHAIN_CONTRACT_ADDRESS'),
        'BLOCKCHAIN_PRIVATE_KEY': os.getenv('BLOCKCHAIN_PRIVATE_KEY'),
        'BLOCKCHAIN_CHAIN_ID': os.getenv('BLOCKCHAIN_CHAIN_ID')
    }
    
    print("\nBlockchain Configuration Status:")
    print("=" * 60)
    
    all_configured = True
    for var, value in required_vars.items():
        if value:
            # Mask sensitive values
            if 'PRIVATE_KEY' in var:
                display_value = value[:10] + "..." + value[-8:] if len(value) > 18 else "***"
            else:
                display_value = value
            print(f"[OK] {var}: {display_value}")
        else:
            print(f"[ERROR] {var}: Not set")
            all_configured = False
    
    print("=" * 60)
    
    if all_configured:
        print("\n[OK] All blockchain variables are configured!")
        return True
    else:
        print("\n[ERROR] Some blockchain variables are missing")
        print("\nAdd them to your .env.mysql file:")
        print("\n# Blockchain Configuration")
        print("BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID")
        print("BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138")
        print("BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE")
        print("BLOCKCHAIN_CHAIN_ID=11155111")
        return False

def test_connection():
    """Test blockchain connection"""
    try:
        from blockchain_logger import is_blockchain_configured, _init_web3
        from blockchain_logger import _web3
        
        _init_web3()
        
        if is_blockchain_configured():
            print("\n[OK] Blockchain is properly configured and connected!")
            
            # Test connection
            if _web3 and _web3.is_connected():
                latest_block = _web3.eth.get_block('latest')
                print(f"[OK] Connected to blockchain")
                print(f"   Latest block: {latest_block.number}")
                print(f"   Network: {'Sepolia Testnet' if _web3.eth.chain_id == 11155111 else 'Other'}")
                return True
            else:
                print("[ERROR] Cannot connect to blockchain RPC")
                return False
        else:
            print("\n[ERROR] Blockchain is not properly configured")
            return False
    except Exception as e:
        print(f"\n[ERROR] Error testing connection: {e}")
        return False

def generate_wallet():
    """Generate a new Ethereum wallet"""
    try:
        from eth_account import Account
        import secrets
        
        print("\nGenerating new Ethereum wallet...")
        print("=" * 60)
        
        # Generate private key
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        
        # Create account
        account = Account.from_key(private_key)
        
        print("NEW WALLET GENERATED")
        print("=" * 60)
        print(f"Address:     {account.address}")
        print(f"Private Key: {private_key}")
        print("=" * 60)
        print("\nIMPORTANT:")
        print("1. Save this private key securely")
        print("2. Never share it or commit to Git")
        print("3. Add it to your .env.mysql file")
        print("4. Get testnet ETH from: https://sepoliafaucet.com/")
        print("=" * 60)
        
        return account.address, private_key
    except ImportError:
        print("[ERROR] eth_account not installed")
        print("Install with: pip install eth-account")
        return None, None

def main():
    """Main function"""
    print("SecureCloud Blockchain Setup Helper")
    print("=" * 60)
    
    # Check web3
    if not check_web3_installed():
        response = input("\nWould you like to install web3 now? (y/n): ")
        if response.lower() == 'y':
            os.system("pip install web3==6.20.1")
            if not check_web3_installed():
                print("\n❌ Installation failed. Please install manually.")
                return
    
    # Check env file
    if not check_env_file():
        return
    
    # Check configuration
    is_configured = check_blockchain_config()
    
    if is_configured:
        # Test connection
        test_connection()
    else:
        print("\nSetup Instructions:")
        print("1. Get Infura account: https://infura.io")
        print("2. Create wallet (use MetaMask or run this script with --generate-wallet)")
        print("3. Get testnet ETH: https://sepoliafaucet.com/")
        print("4. Add variables to .env.mysql")
        print("5. Run this script again to verify")
        
        response = input("\nWould you like to generate a new wallet? (y/n): ")
        if response.lower() == 'y':
            generate_wallet()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-wallet":
        generate_wallet()
    else:
        main()
