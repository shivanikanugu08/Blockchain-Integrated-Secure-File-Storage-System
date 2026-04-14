# Complete Blockchain Integration Guide

Follow these steps to enable blockchain logging for your SecureCloud application.

## Step 1: Install Web3 Library

```bash
pip install web3==6.20.1
```

**Note for Windows users**: If installation fails, you may need to install Visual C++ Build Tools. The app will continue to work without blockchain if web3 fails to install.

## Step 2: Get Infura Account (Free)

1. Go to [https://infura.io](https://infura.io)
2. Click "Get Started for Free"
3. Sign up with your email
4. Verify your email address
5. Log in to your dashboard
6. Click "Create New Key"
7. Select "Web3 API" as the product
8. Name it "SecureCloud" (or any name)
9. Select "Sepolia" network (for testnet)
10. Copy your **Project ID** (you'll see it in the format: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`)

## Step 3: Create Ethereum Wallet

You need a wallet with a private key. Here are two options:

### Option A: Use MetaMask (Recommended for beginners)

1. Install [MetaMask](https://metamask.io) browser extension
2. Create a new wallet (or use existing)
3. Switch to "Sepolia Test Network"
4. Click the three dots next to your account name
5. Select "Account Details"
6. Click "Show Private Key"
7. Enter your password
8. **Copy the private key** (starts with `0x`)
9. **IMPORTANT**: Create a NEW wallet just for this app - don't use your main wallet!

### Option B: Generate Wallet Programmatically

Run this Python script to generate a new wallet:

```python
from eth_account import Account
import secrets

# Generate a new private key
priv = secrets.token_hex(32)
private_key = "0x" + priv

# Create account from private key
account = Account.from_key(private_key)

print("=" * 60)
print("NEW WALLET GENERATED - SAVE THIS INFORMATION!")
print("=" * 60)
print(f"Address: {account.address}")
print(f"Private Key: {private_key}")
print("=" * 60)
print("\n⚠️  WARNING: Keep your private key SECRET!")
print("⚠️  Never share it or commit it to version control!")
print("=" * 60)
```

Save the address and private key securely.

## Step 4: Get Testnet ETH

1. Go to [Sepolia Faucet](https://sepoliafaucet.com/)
2. Enter your wallet address (from Step 3)
3. Request testnet ETH (usually 0.5 ETH)
4. Wait a few minutes for the transaction to complete
5. Verify on [Sepolia Etherscan](https://sepolia.etherscan.io/) by searching your address

**Alternative Faucets**:
- [Alchemy Sepolia Faucet](https://sepoliafaucet.com/)
- [PoW Faucet](https://sepolia-faucet.pk910.de/)

## Step 5: Deploy Smart Contract (or Use Existing)

### Option A: Use Pre-Deployed Contract (Easiest)

The contract is already deployed at:
```
0xd9145CCE52D386f254917e481eB44e9943F39138
```

You can use this address directly in your `.env.mysql` file.

### Option B: Deploy Your Own Contract

1. Go to [Remix IDE](https://remix.ethereum.org)
2. Create a new file: `FileAudit.sol`
3. Copy the contract code from `FileAudit.sol` in your project
4. In the "Solidity Compiler" tab:
   - Select compiler version: `0.8.20` or higher
   - Click "Compile FileAudit.sol"
5. In the "Deploy & Run Transactions" tab:
   - Environment: Select "Injected Provider - MetaMask"
   - Make sure MetaMask is connected to Sepolia network
   - Contract: Select "FileAudit"
   - Click "Deploy"
   - Confirm the transaction in MetaMask
6. After deployment, copy the **Contract Address**
7. Verify on [Sepolia Etherscan](https://sepolia.etherscan.io/)

## Step 6: Update Environment Variables

Edit your `.env.mysql` file and add:

```env
# Blockchain Configuration
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
BLOCKCHAIN_CHAIN_ID=11155111
```

**Replace**:
- `YOUR_INFURA_PROJECT_ID` with your Infura Project ID from Step 2
- `0xYOUR_PRIVATE_KEY_HERE` with your private key from Step 3
- Contract address if you deployed your own (otherwise use the one above)

## Step 7: Test the Configuration

1. Restart your Flask application
2. Upload a file
3. Check the console for blockchain messages like:
   ```
   [Blockchain] Submitted UPLOAD event tx: 0x...
   ```
4. Visit `/blockchain/activity` to see your blockchain records

## Step 8: Verify on Etherscan

1. Go to [Sepolia Etherscan](https://sepolia.etherscan.io/)
2. Search for your contract address
3. Click "Events" tab
4. You should see `FileActionRecorded` events

## Troubleshooting

### "Blockchain not configured" still showing
- Check all 4 environment variables are set in `.env.mysql`
- Restart the Flask application
- Verify no typos in variable names

### "web3 not installed" error
```bash
pip install web3==6.20.1
```

### "Insufficient funds" error
- Get more testnet ETH from faucets
- Check your wallet has ETH on Sepolia network

### "Contract not found" error
- Verify contract address is correct
- Make sure contract is deployed on Sepolia network
- Check contract address on Etherscan

### Transaction fails
- Check you have enough ETH for gas fees
- Verify RPC URL is correct
- Ensure CHAIN_ID matches network (11155111 for Sepolia)

## Security Best Practices

1. ✅ **Never commit `.env.mysql` to Git** (already in .gitignore)
2. ✅ **Use a dedicated wallet** (not your main wallet)
3. ✅ **Use testnet for development** (Sepolia)
4. ✅ **Keep private key secure** (use environment variables, not code)
5. ✅ **Rotate keys if compromised**
6. ✅ **Use mainnet only in production** (with proper security)

## Network Chain IDs

- **Ethereum Mainnet**: `1`
- **Sepolia Testnet**: `11155111` (recommended for testing)
- **Goerli Testnet**: `5` (deprecated)
- **Local/Hardhat**: `31337`

## What Gets Recorded on Blockchain?

- **File Upload**: File ID, user hash, file hash, timestamp
- **File Download**: Access record with timestamp
- **File Delete**: Deletion record (hash preserved)
- **File Share**: Sharing action recorded

All records are **immutable** and **tamper-proof**!

## Next Steps

After setup:
1. Upload a test file
2. Check `/blockchain/activity` page
3. Verify file integrity at `/blockchain/verify/<file_id>`
4. View file history at `/blockchain/history/<file_id>`

## Support

If you encounter issues:
1. Check console logs for blockchain errors
2. Verify all environment variables
3. Test RPC connection: `curl https://sepolia.infura.io/v3/YOUR_PROJECT_ID`
4. Check contract on Etherscan
5. Verify wallet has testnet ETH

---

**Ready to start?** Follow the steps above, and your blockchain integration will be complete! 🚀
