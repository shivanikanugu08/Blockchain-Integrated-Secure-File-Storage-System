import os
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    from web3 import Web3
    from web3.exceptions import ContractLogicError
except Exception:
    # web3 (and its native deps like ckzg) may not be installed or may fail
    # to import on some platforms (e.g. Python 3.13 on Windows without a C
    # compiler). In that case we simply disable blockchain logging.
    Web3 = None  # type: ignore[assignment]
    ContractLogicError = Exception  # type: ignore[assignment]


RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL")
CONTRACT_ADDRESS = os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
CHAIN_ID = int(os.getenv("BLOCKCHAIN_CHAIN_ID", "0"))


_web3: Optional["Web3"] = None  # type: ignore[name-defined]
_contract = None


_CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "fileId", "type": "uint256"},
            {"internalType": "bytes32", "name": "userHash", "type": "bytes32"},
            {"internalType": "string", "name": "action", "type": "string"},
            {"internalType": "bytes32", "name": "fileHash", "type": "bytes32"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "name": "recordFileAction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "fileId", "type": "uint256"},
            {"indexed": True, "internalType": "bytes32", "name": "userHash", "type": "bytes32"},
            {"indexed": False, "internalType": "string", "name": "action", "type": "string"},
            {"indexed": False, "internalType": "bytes32", "name": "fileHash", "type": "bytes32"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "name": "FileActionRecorded",
        "type": "event",
    }
]


def _init_web3():
    """Lazy-init Web3 and contract instance."""
    global _web3, _contract

    # web3 is not available – leave logging disabled
    if Web3 is None:
        return

    if _web3 is not None:
        return

    if not (RPC_URL and CONTRACT_ADDRESS and PRIVATE_KEY and CHAIN_ID):
        # Missing config – leave disabled, app should continue without blockchain
        return

    _web3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not _web3.is_connected():
        # Don't raise – just disable blockchain logging
        _web3 = None
        return

    contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)
    _contract = _web3.eth.contract(address=contract_address, abi=_CONTRACT_ABI)


def _to_bytes32_from_hex_or_text(value: str) -> bytes:
    """Convert a hex string (64 chars) or arbitrary text into a bytes32 value."""
    value = (value or "").strip()
    if len(value) == 64 and all(c in "0123456789abcdefABCDEF" for c in value):
        return bytes.fromhex(value)
    return Web3.keccak(text=value)


def record_blockchain_event(action: str, file_id: int, user_id: int, file_hash: str) -> None:
    """
    Record a file-related event on the Ethereum blockchain.

    This is best-effort: failures are logged to stdout but do not raise.
    """
    _init_web3()
    if _web3 is None or _contract is None:
        # Blockchain logging not configured or unavailable
        return

    try:
        account = _web3.eth.account.from_key(PRIVATE_KEY)
        sender = account.address

        user_hash = Web3.keccak(text=str(user_id))
        file_hash_bytes32 = _to_bytes32_from_hex_or_text(file_hash)
        timestamp = int(_web3.eth.get_block("latest").timestamp)

        nonce = _web3.eth.get_transaction_count(sender)
        gas_price = _web3.eth.gas_price

        tx = _contract.functions.recordFileAction(
            int(file_id),
            user_hash,
            str(action),
            file_hash_bytes32,
            timestamp,
        ).build_transaction(
            {
                "from": sender,
                "nonce": nonce,
                "gasPrice": gas_price,
                "chainId": CHAIN_ID,
            }
        )

        # Estimate and set gas limit
        try:
            gas_estimate = _web3.eth.estimate_gas(tx)
            tx["gas"] = int(gas_estimate * 1.2)
        except Exception:
            tx["gas"] = 300000

        signed = account.sign_transaction(tx)
        tx_hash = _web3.eth.send_raw_transaction(signed.rawTransaction)
        print(f"[Blockchain] Submitted {action} event tx: {tx_hash.hex()}")

    except ContractLogicError as e:
        print(f"[Blockchain] Contract reverted for {action}: {e}")
    except Exception as e:
        print(f"[Blockchain] Failed to record {action} for file {file_id}: {e}")


def verify_file_integrity(file_id: int, expected_hash: str) -> Dict[str, Any]:
    """
    Verify file integrity by checking blockchain records.
    Returns dict with verification status and blockchain records.
    """
    _init_web3()
    if _web3 is None or _contract is None:
        return {
            "verified": False,
            "error": "Blockchain not configured",
            "records": []
        }
    
    try:
        # Query events for this file
        events = _contract.events.FileActionRecorded.get_logs(
            fromBlock=0,
            argument_filters={"fileId": file_id}
        )
        
        if not events:
            return {
                "verified": False,
                "error": "No blockchain records found for this file",
                "records": []
            }
        
        # Get the most recent upload record
        upload_records = [e for e in events if e.args.action == "UPLOAD"]
        if not upload_records:
            return {
                "verified": False,
                "error": "No upload record found on blockchain",
                "records": []
            }
        
        latest_upload = max(upload_records, key=lambda x: x.args.timestamp)
        blockchain_hash = latest_upload.args.fileHash.hex()
        
        # Compare hashes
        expected_hash_bytes = _to_bytes32_from_hex_or_text(expected_hash)
        expected_hash_hex = expected_hash_bytes.hex()
        
        verified = blockchain_hash == expected_hash_hex
        
        # Format records
        records = []
        for event in events:
            records.append({
                "action": event.args.action,
                "fileId": event.args.fileId,
                "fileHash": event.args.fileHash.hex(),
                "timestamp": datetime.fromtimestamp(event.args.timestamp),
                "blockNumber": event.blockNumber,
                "transactionHash": event.transactionHash.hex()
            })
        
        return {
            "verified": verified,
            "blockchain_hash": blockchain_hash,
            "expected_hash": expected_hash_hex,
            "records": sorted(records, key=lambda x: x["timestamp"], reverse=True),
            "latest_upload": {
                "hash": blockchain_hash,
                "timestamp": datetime.fromtimestamp(latest_upload.args.timestamp),
                "blockNumber": latest_upload.blockNumber
            }
        }
        
    except Exception as e:
        return {
            "verified": False,
            "error": str(e),
            "records": []
        }


def get_file_blockchain_history(file_id: int) -> List[Dict[str, Any]]:
    """
    Get complete blockchain history for a file.
    """
    _init_web3()
    if _web3 is None or _contract is None:
        return []
    
    try:
        events = _contract.events.FileActionRecorded.get_logs(
            fromBlock=0,
            argument_filters={"fileId": file_id}
        )
        
        history = []
        for event in events:
            history.append({
                "action": event.args.action,
                "fileId": event.args.fileId,
                "fileHash": event.args.fileHash.hex(),
                "userHash": event.args.userHash.hex(),
                "timestamp": datetime.fromtimestamp(event.args.timestamp),
                "blockNumber": event.blockNumber,
                "transactionHash": event.transactionHash.hex()
            })
        
        return sorted(history, key=lambda x: x["timestamp"], reverse=True)
        
    except Exception as e:
        print(f"[Blockchain] Error fetching history for file {file_id}: {e}")
        return []


def get_user_blockchain_activity(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get blockchain activity for a user.
    """
    _init_web3()
    if _web3 is None or _contract is None:
        return []
    
    try:
        user_hash = Web3.keccak(text=str(user_id))
        events = _contract.events.FileActionRecorded.get_logs(
            fromBlock=0,
            argument_filters={"userHash": user_hash}
        )
        
        activity = []
        for event in events[:limit]:
            activity.append({
                "action": event.args.action,
                "fileId": event.args.fileId,
                "fileHash": event.args.fileHash.hex(),
                "timestamp": datetime.fromtimestamp(event.args.timestamp),
                "blockNumber": event.blockNumber,
                "transactionHash": event.transactionHash.hex()
            })
        
        return sorted(activity, key=lambda x: x["timestamp"], reverse=True)
        
    except Exception as e:
        print(f"[Blockchain] Error fetching activity for user {user_id}: {e}")
        return []


def is_blockchain_configured() -> bool:
    """Check if blockchain is properly configured."""
    _init_web3()
    return _web3 is not None and _contract is not None

