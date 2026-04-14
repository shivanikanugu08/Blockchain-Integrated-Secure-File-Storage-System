#!/usr/bin/env python3
"""
Add blockchain configuration to .env.mysql file
"""

import os
from pathlib import Path

def add_blockchain_config():
    """Add blockchain configuration to .env.mysql"""
    env_file = Path('.env.mysql')
    
    if not env_file.exists():
        print("[ERROR] .env.mysql file not found!")
        print("Create it first with your MySQL configuration.")
        return False
    
    # Read existing file
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Check if blockchain config already exists
    if 'BLOCKCHAIN_RPC_URL' in content:
        print("[INFO] Blockchain configuration already exists in .env.mysql")
        response = input("Do you want to update it? (y/n): ")
        if response.lower() != 'y':
            return False
        
        # Remove existing blockchain config
        lines = content.split('\n')
        new_lines = []
        skip_blockchain = False
        for line in lines:
            if line.strip().startswith('# Blockchain'):
                skip_blockchain = True
            elif skip_blockchain and line.strip() and not line.strip().startswith('#'):
                if not line.strip().startswith('BLOCKCHAIN_'):
                    skip_blockchain = False
                    new_lines.append(line)
                # Skip blockchain lines
                continue
            else:
                if not skip_blockchain:
                    new_lines.append(line)
        content = '\n'.join(new_lines)
    
    # Get configuration from user
    print("\n" + "="*60)
    print("Blockchain Configuration Setup")
    print("="*60)
    print("\nEnter your blockchain configuration:")
    print("(Press Enter to use default/pre-filled values)\n")
    
    # Get Infura Project ID
    rpc_url = input("Infura RPC URL (e.g., https://sepolia.infura.io/v3/YOUR_PROJECT_ID): ").strip()
    if not rpc_url:
        project_id = input("Or enter just your Infura Project ID: ").strip()
        if project_id:
            rpc_url = f"https://sepolia.infura.io/v3/{project_id}"
        else:
            print("[SKIP] RPC URL not set. Add it manually later.")
            rpc_url = ""
    
    # Contract address
    contract = input("Contract Address [default: 0xd9145CCE52D386f254917e481eB44e9943F39138]: ").strip()
    if not contract:
        contract = "0xd9145CCE52D386f254917e481eB44e9943F39138"
    
    # Private key
    private_key = input("Private Key (0x...): ").strip()
    if not private_key:
        print("[SKIP] Private key not set. Add it manually later.")
        private_key = ""
    
    # Chain ID
    chain_id = input("Chain ID [default: 11155111 for Sepolia]: ").strip()
    if not chain_id:
        chain_id = "11155111"
    
    # Append blockchain config
    blockchain_config = f"""
# Blockchain Configuration
BLOCKCHAIN_RPC_URL={rpc_url}
BLOCKCHAIN_CONTRACT_ADDRESS={contract}
BLOCKCHAIN_PRIVATE_KEY={private_key}
BLOCKCHAIN_CHAIN_ID={chain_id}
"""
    
    # Add to file
    with open(env_file, 'a') as f:
        f.write(blockchain_config)
    
    print("\n[SUCCESS] Blockchain configuration added to .env.mysql")
    print("\nNext steps:")
    print("1. Verify the configuration is correct")
    print("2. Install web3: pip install web3==6.20.1")
    print("3. Restart your Flask app")
    print("4. Test by uploading a file")
    
    return True

if __name__ == "__main__":
    try:
        add_blockchain_config()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Configuration not saved.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
