// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EvidenceRegistry {

    struct Evidence {
        string cid;
        string evidenceHash;
        uint256 timestamp;
        string personDetected;
    }

    uint256 public evidenceCount;
    mapping(uint256 => Evidence) public evidences;

    function storeEvidence(
        string memory _cid,
        string memory _hash,
        string memory _personDetected
    ) public {

        evidenceCount = evidenceCount + 1;
        evidences[evidenceCount] = Evidence({
            cid: _cid,
            evidenceHash: _hash,
            timestamp: block.timestamp,
            personDetected: _personDetected
        });
    }

    function getEvidence(uint256 _evidenceId)
        public
        view
        returns (
            string memory,
            string memory,
            uint256,
            string memory
        )
    {
        return (
            evidences[_evidenceId].cid,
            evidences[_evidenceId].evidenceHash,
            evidences[_evidenceId].timestamp,
            evidences[_evidenceId].personDetected
        );
    }

    function getEvidenceCount()
        public
        view
        returns (uint256)
    {
        return evidenceCount;
    }
}