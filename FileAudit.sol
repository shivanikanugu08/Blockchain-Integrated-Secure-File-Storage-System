// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileAudit {
    event FileActionRecorded(
        uint256 indexed fileId,
        bytes32 indexed userHash,
        string action,
        bytes32 fileHash,
        uint256 timestamp
    );

    function recordFileAction(
        uint256 fileId,
        bytes32 userHash,
        string calldata action,
        bytes32 fileHash,
        uint256 timestamp
    ) external {
        emit FileActionRecorded(fileId, userHash, action, fileHash, timestamp);
    }
}

