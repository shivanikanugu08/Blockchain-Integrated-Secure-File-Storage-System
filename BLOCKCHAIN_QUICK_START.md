# Blockchain Integration - Quick Start Guide

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Web3 (May Require Build Tools on Windows)

**For Windows:**
```bash
# Option 1: Try installing (may fail without C++ tools)
pip install web3==6.20.1

# Option 2: If it fails, install Visual C++ Build Tools first:
# Download from: https://visualstudio.microsoft.com/downloads/
# Install "Desktop development with C++" workload
# Then retry: pip install web3==6.20.1

# Option 3: Use WSL (Windows Subsystem for Linux)
# This avoids the build tools requirement
```

**For Linux/Mac:**
```bash
pip install web3==6.20.1
```

**Note:** If web3 installation fails, your app will still work - blockchain features will just be disabled. You can configure blockchain later.

### Step 2: Get Infura Account (2 minutes)

1. Visit: https://infura.io
2. Sign up (free)
3. Create new project → Select "Web3 API"
4. Choose "Sepolia" network
5. Copy your **Project ID**

### Step 3: Create Wallet & Get Testnet ETH (3 minutes)

**Option A: Use MetaMask (Easiest)**
1. Install MetaMask: https://metamask.io
2. Create wallet → Switch to "Sepolia Test Network"
3. Get private key: Account → Account Details → Show Private Key
4. Get testnet ETH: https://sepoliafaucet.com/ (enter your address)

**Option B: Generate Wallet with Python**
```python
from eth_account import Account
import secrets

priv = secrets.token_hex(32)
private_key = "0x" + priv
account = Account.from_key(private_key)

print(f"Address: {account.address}")
print(f"Private Key: {private_key}")
# Get ETH at: https://sepoliafaucet.com/
```

### Step 4: Update .env.mysql

Add these lines to your `.env.mysql` file:

```env
# Blockchain Configuration
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
BLOCKCHAIN_CHAIN_ID=11155111
```

**Replace:**
- `YOUR_INFURA_PROJECT_ID` → Your Infura Project ID
- `0xYOUR_PRIVATE_KEY_HERE` → Your wallet private key

### Step 5: Restart Application

```bash
python run_mysql.py
```

### Step 6: Test It!

1. Upload a file
2. Check console for: `[Blockchain] Submitted UPLOAD event tx: 0x...`
3. Visit: `http://localhost:5000/blockchain/activity`

## ✅ Verification Checklist

- [ ] web3 installed (or app runs without errors)
- [ ] Infura account created
- [ ] Wallet created with testnet ETH
- [ ] All 4 variables added to `.env.mysql`
- [ ] Application restarted
- [ ] Uploaded test file
- [ ] Blockchain activity visible

## 🔧 Troubleshooting

### "web3 installation failed" (Windows)
- **Solution 1:** Install Visual Studio Build Tools
- **Solution 2:** Use WSL (Windows Subsystem for Linux)
- **Solution 3:** Continue without blockchain (app works fine)

### "Blockchain not configured"
- Check all 4 variables in `.env.mysql`
- Restart application
- Verify no typos

### "Insufficient funds"
- Get more testnet ETH from faucets
- Check wallet on Sepolia Etherscan

### "Cannot connect to RPC"
- Verify Infura Project ID is correct
- Check internet connection
- Try different RPC endpoint

## 📚 Full Documentation

See `BLOCKCHAIN_SETUP_GUIDE.md` for detailed instructions.

## 🚀 Ready to Go!

Once configured, all file actions (upload, download, delete, share) will be automatically recorded on the blockchain!
