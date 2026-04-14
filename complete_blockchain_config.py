#!/usr/bin/env python3
"""
Complete blockchain configuration - Add missing values
"""

from pathlib import Path
import re

def update_blockchain_config():
    """Update blockchain configuration in .env.mysql"""
    env_file = Path('.env.mysql')
    
    if not env_file.exists():
        print("[ERROR] .env.mysql file not found!")
        return False
    
    # Read file
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Check current status
    has_rpc = 'BLOCKCHAIN_RPC_URL=' in content and 'BLOCKCHAIN_RPC_URL=$' not in content
    has_private_key = 'BLOCKCHAIN_PRIVATE_KEY=' in content and len(re.findall(r'BLOCKCHAIN_PRIVATE_KEY=0x[a-fA-F0-9]{64}', content)) > 0
    
    print("Current Configuration Status:")
    print(f"  RPC URL: {'[OK]' if has_rpc else '[MISSING]'}")
    print(f"  Private Key: {'[OK]' if has_private_key else '[MISSING]'}")
    print(f"  Contract Address: [OK] (using default)")
    print(f"  Chain ID: [OK] (using default)")
    print()
    
    # Get missing values
    updates = {}
    
    if not has_rpc:
        print("="*60)
        print("Step 1: Infura RPC URL")
        print("="*60)
        print("\nGet your Infura Project ID:")
        print("1. Visit: https://infura.io")
        print("2. Sign up (free) or log in")
        print("3. Create new project → Web3 API → Sepolia")
        print("4. Copy your Project ID\n")
        
        project_id = input("Enter your Infura Project ID (or press Enter to skip): ").strip()
        if project_id:
            updates['BLOCKCHAIN_RPC_URL'] = f"https://sepolia.infura.io/v3/{project_id}"
            print(f"[OK] RPC URL will be set to: {updates['BLOCKCHAIN_RPC_URL']}")
        else:
            print("[SKIP] RPC URL not updated")
    
    if not has_private_key:
        print("\n" + "="*60)
        print("Step 2: Ethereum Wallet Private Key")
        print("="*60)
        print("\nOptions:")
        print("1. Use MetaMask: Install → Create wallet → Export private key")
        print("2. Generate new wallet (I can help with this)")
        print("3. Skip and add manually later\n")
        
        choice = input("Enter private key (0x...), 'generate' to create new, or press Enter to skip: ").strip()
        
        if choice.lower() == 'generate':
            try:
                from eth_account import Account
                import secrets
                
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
                print("1. Save this private key securely!")
                print("2. Get testnet ETH from: https://sepoliafaucet.com/")
                print("3. Enter your wallet address to get ETH")
                print("="*60)
                
                updates['BLOCKCHAIN_PRIVATE_KEY'] = private_key
                print(f"\n[OK] Private key will be added to .env.mysql")
                
            except ImportError:
                print("[ERROR] eth_account not installed")
                print("Install with: pip install eth-account")
                print("Or use MetaMask to get a private key")
        elif choice.startswith('0x') and len(choice) == 66:
            updates['BLOCKCHAIN_PRIVATE_KEY'] = choice
            print("[OK] Private key will be added")
        else:
            print("[SKIP] Private key not updated")
    
    # Update file
    if updates:
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            for key, value in updates.items():
                if line.startswith(f"{key}="):
                    line = f"{key}={value}"
                    break
            new_lines.append(line)
        
        with open(env_file, 'w') as f:
            f.write('\n'.join(new_lines))
        
        print("\n[SUCCESS] Configuration updated!")
        print("\nUpdated values:")
        for key, value in updates.items():
            if 'PRIVATE_KEY' in key:
                display = value[:10] + "..." + value[-8:]
            else:
                display = value
            print(f"  {key}: {display}")
    else:
        print("\n[INFO] No updates needed or all values skipped")
    
    # Final checklist
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("1. Install web3: pip install web3==6.20.1")
    print("2. Get testnet ETH (if you generated wallet):")
    print("   - Visit: https://sepoliafaucet.com/")
    print("   - Enter your wallet address")
    print("3. Verify configuration:")
    print("   - Run: python integrate_blockchain.py")
    print("4. Restart Flask app")
    print("5. Test by uploading a file")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        update_blockchain_config()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Configuration not updated.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
