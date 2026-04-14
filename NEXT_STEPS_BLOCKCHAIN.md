# Complete Your Blockchain Configuration

## ✅ What's Done
- Contract Address: ✅ Configured
- Chain ID: ✅ Configured (Sepolia testnet)

## ❌ What's Missing
- RPC URL: Need Infura Project ID
- Private Key: Need Ethereum wallet

---

## Step 1: Get Infura RPC URL (2 minutes)

1. **Visit:** https://infura.io
2. **Sign up** (free account)
3. **Create new project:**
   - Click "Create New Key"
   - Product: Select "Web3 API"
   - Network: Select "Sepolia"
   - Name: "SecureCloud"
4. **Copy your Project ID**

Then add to `.env.mysql`:
```env
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
```

**OR** run the completion script:
```bash
python complete_blockchain_config.py
```

---

## Step 2: Get Ethereum Wallet Private Key (3 minutes)

### Option A: Use MetaMask (Easiest)
1. Install: https://metamask.io
2. Create wallet
3. Switch to "Sepolia Test Network"
4. Export private key:
   - Click account icon → Account Details
   - Show Private Key → Enter password
   - Copy the private key (starts with `0x`)

### Option B: Generate New Wallet
```bash
# First install eth-account
pip install eth-account

# Then generate wallet
python complete_blockchain_config.py
# Choose 'generate' when prompted
```

Then add to `.env.mysql`:
```env
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
```

---

## Step 3: Get Testnet ETH (1 minute)

1. **Go to:** https://sepoliafaucet.com/
2. **Enter your wallet address** (from MetaMask or generated wallet)
3. **Request testnet ETH** (usually 0.5 ETH)
4. **Wait 1-2 minutes** for transaction

---

## Step 4: Complete Configuration

### Quick Method:
```bash
python complete_blockchain_config.py
```

This will:
- Ask for your Infura Project ID
- Help you generate a wallet (or enter existing private key)
- Update `.env.mysql` automatically

### Manual Method:
Edit `.env.mysql` and update these lines:
```env
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY
```

---

## Step 5: Install Web3

```bash
pip install web3==6.20.1
```

**If it fails on Windows:**
- Install Visual C++ Build Tools: https://visualstudio.microsoft.com/downloads/
- Or continue without blockchain (app works fine)

---

## Step 6: Verify Configuration

```bash
python integrate_blockchain.py
```

You should see all ✅ marks!

---

## Step 7: Test Blockchain

1. **Restart Flask app:**
   ```bash
   python run_mysql.py
   ```

2. **Upload a test file**
   - Login to your app
   - Upload any file
   - Check console for: `[Blockchain] Submitted UPLOAD event tx: 0x...`

3. **View blockchain activity:**
   - Visit: `http://localhost:5000/blockchain/activity`
   - You should see your file actions!

---

## Quick Command Summary

```bash
# Complete missing configuration
python complete_blockchain_config.py

# Verify setup
python integrate_blockchain.py

# Install web3
pip install web3==6.20.1

# Restart app
python run_mysql.py
```

---

## Need Help?

- **Infura setup:** https://infura.io/docs
- **MetaMask:** https://metamask.io
- **Testnet faucet:** https://sepoliafaucet.com/
- **Full guide:** See `BLOCKCHAIN_QUICK_SETUP.md`

---

**You're almost there!** Just need to add the RPC URL and private key! 🚀
