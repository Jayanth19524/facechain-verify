from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class FaceCandidate:
    person_detected: str
    matched_page: str
    candidate_image: str
    candidate_path: str
    similarity: float = 0.0
    verified: bool = False

@dataclass
class SearchResult:
    person_detected: str
    candidates: List[FaceCandidate]

@dataclass
class VerificationResult:
    person_detected: str
    matched_page: str
    candidate_image: str
    similarity: float
    verified: bool
    total_candidates_evaluated: int
    best_candidate_index: int

@dataclass
class EvidenceRecord:
    person_detected: str
    matched_page: str
    candidate_image: str
    candidate_path: str
    similarity: float
    verified: bool
    threshold: float
    total_candidates_evaluated: int
    best_candidate_index: int
    timestamp: str
    input_image: str

@dataclass
class BlockchainRecord:
    cid: str
    evidence_hash: str
    timestamp: int
