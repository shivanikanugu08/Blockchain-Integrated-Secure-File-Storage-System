# Blockchain Integration - Quick Setup

## ✅ Good News!

The blockchain code is **already integrated** in your app! You just need to configure it.

## 🚀 Quick Setup (5 Minutes)

### 1. Install Web3 (1 min)

```bash
pip install web3==6.20.1
```

**If it fails on Windows:** Install Visual C++ Build Tools first, or continue without blockchain (app works fine).

### 2. Get Infura Account (2 min)

1. Go to: https://infura.io
2. Sign up (free)
3. Create project → Select "Web3 API" → "Sepolia"
4. Copy your **Project ID**

### 3. Create Wallet & Get ETH (2 min)

**Option A: MetaMask**
- Install: https://metamask.io
- Create wallet → Switch to Sepolia network
- Export private key
- Get ETH: https://sepoliafaucet.com/

**Option B: Generate Wallet**
```bash
python integrate_blockchain.py --generate-wallet
```
(Requires: `pip install eth-account`)

### 4. Add to .env.mysql

**Option A: Use Helper Script**
```bash
python add_blockchain_config.py
```

**Option B: Manual Edit**
Add to `.env.mysql`:
```env
# Blockchain Configuration
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY
BLOCKCHAIN_CHAIN_ID=11155111
```

### 5. Verify & Test

```bash
# Check configuration
python integrate_blockchain.py

# Restart app
python run_mysql.py

# Upload a file and check console for blockchain messages
```

## 📋 Configuration Checklist

- [ ] web3 installed (`pip install web3==6.20.1`)
- [ ] Infura account created
- [ ] Wallet created with testnet ETH
- [ ] All 4 variables in `.env.mysql`
- [ ] App restarted
- [ ] Test file uploaded
- [ ] Blockchain activity visible

## 🎯 What's Already Integrated

✅ File upload logging
✅ File download logging  
✅ File delete logging
✅ File share logging
✅ Integrity verification
✅ Blockchain activity page (`/blockchain/activity`)
✅ File history endpoint (`/blockchain/history/<id>`)
✅ Verification endpoint (`/blockchain/verify/<id>`)

## 📚 Detailed Guides

- **BLOCKCHAIN_INTEGRATION_STEPS.md** - Complete step-by-step guide
- **BLOCKCHAIN_QUICK_START.md** - Quick reference
- **BLOCKCHAIN_SETUP_GUIDE.md** - Detailed documentation

## ⚠️ Important

- Never commit `.env.mysql` to Git
- Use dedicated wallet (not main wallet)
- Use testnet for development
- Keep private key secure

## 🆘 Troubleshooting

**"web3 not installed"** → Install Visual C++ Build Tools or use WSL

**"Blockchain not configured"** → Check all 4 variables in `.env.mysql`

**"Insufficient funds"** → Get testnet ETH from faucets

**No transactions** → Check wallet has ETH, verify RPC URL

---

**Ready?** Start with Step 1 above! 🚀
