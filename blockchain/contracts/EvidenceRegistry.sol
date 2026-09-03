// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EvidenceRegistry {

    struct Evidence {
        string cid;
        string evidenceHash;
        uint256 timestamp;
    }

    Evidence public evidence;

    function storeEvidence(
        string memory _cid,
        string memory _hash
    ) public {

        evidence = Evidence({
            cid: _cid,
            evidenceHash: _hash,
            timestamp: block.timestamp
        });
    }

    function getEvidence()
        public
        view
        returns (
            string memory,
            string memory,
            uint256
        )
    {
        return (
            evidence.cid,
            evidence.evidenceHash,
            evidence.timestamp
        );
    }
}