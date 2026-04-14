# Blockchain Integration - Step by Step

Follow these steps to complete blockchain integration:

## Current Status
✅ Blockchain code is already integrated in app_mysql.py
✅ Blockchain routes are set up
❌ web3 library needs to be installed
❌ Environment variables need to be configured

---

## Step 1: Install Web3 Library

### Option A: Direct Install (May Fail on Windows)
```bash
pip install web3==6.20.1
```

### Option B: If Installation Fails (Windows)
1. Install Visual C++ Build Tools:
   - Download: https://visualstudio.microsoft.com/downloads/
   - Install "Desktop development with C++" workload
   - Restart computer
   - Then retry: `pip install web3==6.20.1`

### Option C: Use Pre-built Wheel (Advanced)
```bash
pip install --only-binary :all: web3==6.20.1
```

**Note:** Your app will work without web3, but blockchain features will be disabled.

---

## Step 2: Get Infura Account (Free)

1. **Visit:** https://infura.io
2. **Sign up** for free account
3. **Create new project:**
   - Click "Create New Key"
   - Product: Select "Web3 API"
   - Network: Select "Sepolia"
   - Name: "SecureCloud" (or any name)
4. **Copy your Project ID** (you'll see it in the URL format)

---

## Step 3: Create Ethereum Wallet

### Option A: Use MetaMask (Easiest)
1. Install MetaMask: https://metamask.io
2. Create new wallet
3. Switch to "Sepolia Test Network"
4. Get private key:
   - Click account icon → Account Details
   - Show Private Key → Enter password
   - **Copy the private key** (starts with `0x`)
5. **IMPORTANT:** Create a NEW wallet just for this app!

### Option B: Generate with Python
```python
from eth_account import Account
import secrets

priv = secrets.token_hex(32)
private_key = "0x" + priv
account = Account.from_key(private_key)

print(f"Address: {account.address}")
print(f"Private Key: {private_key}")
```

---

## Step 4: Get Testnet ETH

1. **Go to:** https://sepoliafaucet.com/
2. **Enter your wallet address** (from Step 3)
3. **Request testnet ETH** (usually 0.5 ETH)
4. **Wait a few minutes** for transaction
5. **Verify on:** https://sepolia.etherscan.io/ (search your address)

**Alternative Faucets:**
- https://www.alchemy.com/faucets/ethereum-sepolia
- https://sepolia-faucet.pk910.de/

---

## Step 5: Configure Environment Variables

Edit your `.env.mysql` file and add these lines:

```env
# Blockchain Configuration
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
BLOCKCHAIN_CHAIN_ID=11155111
```

**Replace:**
- `YOUR_INFURA_PROJECT_ID` → Your Infura Project ID from Step 2
- `0xYOUR_PRIVATE_KEY_HERE` → Your private key from Step 3

**Example:**
```env
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/abc123def456ghi789
BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138
BLOCKCHAIN_PRIVATE_KEY=0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
BLOCKCHAIN_CHAIN_ID=11155111
```

---

## Step 6: Verify Configuration

Run the integration checker:
```bash
python integrate_blockchain.py
```

You should see:
```
[OK] web3 library is installed
[OK] .env.mysql file found
[OK] BLOCKCHAIN_RPC_URL: https://sepolia.infura.io/v3/...
[OK] BLOCKCHAIN_CONTRACT_ADDRESS: 0xd9145CCE52D386f254917e481eB44e9943F39138
[OK] BLOCKCHAIN_PRIVATE_KEY: 0x1234...5678
[OK] BLOCKCHAIN_CHAIN_ID: 11155111
[OK] Connected to blockchain
```

---

## Step 7: Test Blockchain Integration

1. **Restart your Flask app:**
   ```bash
   python run_mysql.py
   ```

2. **Upload a test file:**
   - Login to your app
   - Upload any file
   - Check console for: `[Blockchain] Submitted UPLOAD event tx: 0x...`

3. **View blockchain activity:**
   - Visit: `http://localhost:5000/blockchain/activity`
   - You should see your file actions recorded

4. **Verify on Etherscan:**
   - Go to: https://sepolia.etherscan.io/
   - Search for contract: `0xd9145CCE52D386f254917e481eB44e9943F39138`
   - Click "Events" tab
   - You should see `FileActionRecorded` events

---

## What Gets Recorded on Blockchain?

✅ **File Uploads** - File ID, user hash, file hash, timestamp
✅ **File Downloads** - Access records
✅ **File Deletions** - Deletion records (hash preserved)
✅ **File Shares** - Sharing actions

All records are **immutable** and **tamper-proof**!

---

## Troubleshooting

### "web3 installation failed"
- Install Visual C++ Build Tools (Windows)
- Or use WSL (Windows Subsystem for Linux)
- App works without blockchain, features just disabled

### "Blockchain not configured"
- Check all 4 variables in `.env.mysql`
- Restart Flask app
- Run `python integrate_blockchain.py` to verify

### "Insufficient funds"
- Get more testnet ETH from faucets
- Check wallet balance on Etherscan

### "Cannot connect to RPC"
- Verify Infura Project ID is correct
- Check internet connection
- Try different RPC endpoint

### No transactions appearing
- Check wallet has testnet ETH
- Verify RPC URL is correct
- Check console for error messages
- Verify contract address is correct

---

## Security Reminders

⚠️ **IMPORTANT:**
- Never commit `.env.mysql` to Git (already in .gitignore)
- Keep private key secure
- Use dedicated wallet (not your main wallet)
- Use testnet for development
- Switch to mainnet only in production

---

## Quick Reference

**Pre-deployed Contract Address:**
```
0xd9145CCE52D386f254917e481eB44e9943F39138
```

**Sepolia Testnet:**
- Chain ID: `11155111`
- RPC: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`
- Explorer: https://sepolia.etherscan.io/

**Mainnet (Production):**
- Chain ID: `1`
- RPC: `https://mainnet.infura.io/v3/YOUR_PROJECT_ID`
- Explorer: https://etherscan.io/

---

## Next Steps After Integration

1. ✅ Upload test files
2. ✅ Check blockchain activity page
3. ✅ Verify file integrity
4. ✅ View file history
5. ✅ Test all file operations (upload, download, delete, share)

---

## Support

If you encounter issues:
1. Run: `python integrate_blockchain.py`
2. Check console logs for blockchain errors
3. Verify environment variables
4. Test RPC connection manually
5. Check contract on Etherscan

**Ready to integrate?** Follow the steps above! 🚀
