# Blockchain Integration Setup Guide

This application uses Ethereum blockchain to record file actions (upload, download, delete, share) for tamper-proof audit trails and integrity verification.

## Features

- ✅ **Immutable Records**: All file actions are recorded on the blockchain
- ✅ **Integrity Verification**: SHA-256 hashes stored on-chain verify file integrity
- ✅ **Tamper Detection**: Any file modification is detectable via blockchain verification
- ✅ **Audit Trail**: Complete history of all file operations
- ✅ **Decentralized Trust**: No single point of failure

## Prerequisites

1. **Ethereum Node Access**: You need access to an Ethereum node (mainnet, testnet, or local)
   - Options: Infura, Alchemy, QuickNode, or your own node
   - For testing: Use Sepolia testnet (free)

2. **Deploy Smart Contract**: Deploy the `FileAudit.sol` contract to your network
   - Contract address: `0xd9145CCE52D386f254917e481eB44e9943F39138` (if already deployed)
   - Or deploy your own using Remix IDE

3. **Funded Account**: An Ethereum account with ETH for gas fees
   - For testnet: Get free ETH from faucets

## Setup Steps

### 1. Install Dependencies

```bash
pip install web3==6.20.1
```

**Note**: On Windows with Python 3.13, `web3` may require C++ build tools. If installation fails, the app will continue without blockchain features.

### 2. Configure Environment Variables

Create or update `.env.mysql` file with:

```bash
# Blockchain Configuration
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
BLOCKCHAIN_CONTRACT_ADDRESS=0xd9145CCE52D386f254917e481eB44e9943F39138
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
BLOCKCHAIN_CHAIN_ID=11155111  # 1 for mainnet, 11155111 for Sepolia
```

### 3. Get Infura Project ID (for testnet)

1. Go to [Infura.io](https://infura.io)
2. Sign up for free account
3. Create a new project
4. Select "Ethereum" network
5. Copy your Project ID
6. Use: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`

### 4. Get Testnet ETH (for Sepolia)

1. Go to [Sepolia Faucet](https://sepoliafaucet.com/)
2. Enter your Ethereum address
3. Request testnet ETH

### 5. Deploy Smart Contract (if needed)

1. Open [Remix IDE](https://remix.ethereum.org)
2. Create new file `FileAudit.sol`
3. Copy contract code from `FileAudit.sol`
4. Compile with Solidity 0.8.x
5. Deploy to Sepolia testnet
6. Copy contract address to `.env.mysql`

## How It Works

### File Upload
1. File is encrypted locally
2. SHA-256 hash of encrypted file is calculated
3. Transaction sent to blockchain with:
   - File ID
   - User hash (privacy-preserving)
   - Action: "UPLOAD"
   - File hash
   - Timestamp

### File Download
1. File integrity verified against stored hash
2. Blockchain verification checks on-chain hash
3. Transaction recorded: "DOWNLOAD"

### File Delete
1. Deletion action recorded on blockchain
2. File hash preserved for audit trail

### Integrity Verification
- Compares current file hash with blockchain record
- Detects any tampering or modification
- Provides immutable proof of file state

## API Endpoints

### Verify File Integrity
```
GET /blockchain/verify/<file_id>
```
Returns JSON with verification status and blockchain records.

### Get File History
```
GET /blockchain/history/<file_id>
```
Returns complete blockchain history for a file.

### View Activity
```
GET /blockchain/activity
```
Shows all blockchain activity for the current user.

## Security Notes

⚠️ **Important**:
- Never commit `.env.mysql` to version control
- Keep your private key secure
- Use testnet for development
- Private key should be for a dedicated account (not your main wallet)

## Troubleshooting

### "Blockchain not configured" warning
- Check that all environment variables are set
- Verify RPC URL is accessible
- Ensure contract address is correct

### Transaction failures
- Check account has sufficient ETH for gas
- Verify network (mainnet vs testnet) matches CHAIN_ID
- Check contract address is correct

### Import errors
- On Windows, `web3` may require Visual C++ Build Tools
- App will continue without blockchain if import fails
- See requirements.txt for dependencies

## Network IDs

- **Mainnet**: Chain ID `1`
- **Sepolia Testnet**: Chain ID `11155111`
- **Goerli Testnet**: Chain ID `5`
- **Local/Hardhat**: Chain ID `31337`

## Smart Contract

The `FileAudit.sol` contract emits events for each file action:
- `FileActionRecorded(fileId, userHash, action, fileHash, timestamp)`

Events are indexed by `fileId` and `userHash` for efficient querying.

## Benefits

1. **Tamper-Proof**: Once recorded, blockchain records cannot be altered
2. **Transparency**: All actions are publicly verifiable
3. **Audit Trail**: Complete history of file operations
4. **Integrity**: SHA-256 hashes ensure file authenticity
5. **Decentralization**: No single point of failure

## Support

For issues or questions:
1. Check blockchain logs in console output
2. Verify environment variables
3. Test RPC connection manually
4. Check contract on Etherscan
