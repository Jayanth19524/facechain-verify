#!/usr/bin/env python3
"""
FaceChain Verify - End-to-end face identification & blockchain verification pipeline.

Searches multiple candidates, picks the best match by similarity, and pushes to blockchain.

Usage:
    python -m pipeline.run_pipeline [options]

Example:
    python -m pipeline.run_pipeline --input samples/face.jpg --threshold 0.6 --verbose
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Optional

from search.vision_search import search_image
from face.verify_match import verify_match


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_step(msg: str):
    print(f"{Colors.CYAN}▶{Colors.RESET} {Colors.BOLD}{msg}{Colors.RESET}")


def print_success(msg: str):
    print(f"{Colors.GREEN}✅{Colors.RESET} {msg}")


def print_error(msg: str):
    print(f"{Colors.RED}❌{Colors.RESET} {msg}", file=sys.stderr)


def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️{Colors.RESET} {msg}")


def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ️{Colors.RESET} {msg}")


def retry_with_backoff(func, max_attempts: int = 3, base_delay: float = 1.0, *args, **kwargs):
    last_exception = None
    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_attempts:
                delay = base_delay * (2 ** (attempt - 1))
                print_warning(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print_error(f"All {max_attempts} attempts failed")
    raise last_exception


def parse_args():
    parser = argparse.ArgumentParser(
        description="FaceChain Verify - Face identification & blockchain verification pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m pipeline.run_pipeline
  python -m pipeline.run_pipeline --input samples/face.jpg --threshold 0.6
  python -m pipeline.run_pipeline --input my_photo.jpg --output-dir my_evidence --verbose
        """
    )
    parser.add_argument(
        "--input", "-i",
        default="samples/face.jpg",
        help="Path to input face image (default: samples/face.jpg)"
    )
    parser.add_argument(
        "--threshold", "-t",
        type=float,
        default=0.60,
        help="Similarity threshold for verification (default: 0.60)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="evidence",
        help="Output directory for evidence files (default: evidence)"
    )
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=8,
        help="Max number of candidate images to evaluate (default: 8)"
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Max retry attempts for API calls (default: 3)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    return parser.parse_args()


def validate_input_image(image_path: str) -> bool:
    if not os.path.exists(image_path):
        print_error(f"Input image not found: {image_path}")
        return False
    if not os.path.isfile(image_path):
        print_error(f"Input path is not a file: {image_path}")
        return False
    return True


def find_best_match(input_image, candidates, threshold):
    print_step("Step 3: Evaluating all candidates...")

    best = None
    best_similarity = 0.0

    for i, cand in enumerate(candidates):
        cand_path = cand["candidate_path"]
        print_info(f"  Evaluating candidate {i+1}/{len(candidates)}: {cand_path}")
        try:
            similarity = retry_with_backoff(
                verify_match, 2, 0.5, input_image, cand_path
            )
            print_info(f"    Similarity: {similarity:.4f}")
            if similarity > best_similarity:
                best_similarity = similarity
                best = cand
                best["similarity"] = round(similarity, 4)
        except Exception as e:
            print_error(f"    Failed to verify candidate {i+1}: {e}")
            continue

    if not best:
        raise Exception("No candidates could be verified")

    verified = best_similarity >= threshold

    print_success(f"Best similarity: {best_similarity:.4f}")
    if verified:
        print_success(f"Above threshold ({threshold}) - VERIFIED")
    else:
        print_warning(f"Below threshold ({threshold}) - NOT VERIFIED")

    return best, best_similarity, verified


def save_evidence(evidence, evidence_path):
    print_step("Step 4: Saving evidence...")
    with open(evidence_path, "w") as f:
        json.dump(evidence, f, indent=2)
    print_success(f"Evidence saved to: {evidence_path}")


def push_to_blockchain(evidence_path):
    print_step("Step 5: Hashing evidence...")
    import subprocess
    result = subprocess.run(
        [sys.executable, "evidence/hash_evidence.py", "--evidence-path", evidence_path],
        capture_output=True, text=True
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print_error(f"Hash failed: {result.stderr}")
        sys.exit(1)

    print_step("Step 6: Uploading to IPFS...")
    result = subprocess.run(
        [sys.executable, "blockchain/upload_ipfs.py"],
        capture_output=True, text=True
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print_error(f"IPFS upload failed: {result.stderr}")
        sys.exit(1)

    print_step("Step 7: Storing on blockchain...")
    result = subprocess.run(
        [sys.executable, "blockchain/store_evidence.py"],
        capture_output=True, text=True
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print_error(f"Blockchain store failed: {result.stderr}")
        sys.exit(1)

    print_success("All blockchain steps completed!")


def main():
    args = parse_args()

    if not validate_input_image(args.input):
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    evidence_path = os.path.join(args.output_dir, "evidence.json")

    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       FaceChain Verify - Pipeline Execution              ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    print_info(f"Input image: {args.input}")
    print_info(f"Similarity threshold: {args.threshold}")
    print_info(f"Max candidates: {args.max_candidates}")
    print_info(f"Output directory: {args.output_dir}")
    print()

    try:
        print_step("Step 1: Searching web for matching content...")
        search_result = retry_with_backoff(
            search_image, args.max_retries, 1.0, args.input, args.max_candidates
        )

        if args.verbose:
            print(json.dumps(search_result, indent=2))

        person = search_result.get("person_detected", "Unknown")
        candidates = search_result.get("candidates", [])

        if not candidates:
            print_error("No candidate images found in search results")
            sys.exit(1)

        print_success(f"Person detected: {person}")
        print_info(f"Candidates collected: {len(candidates)}")
        print()

        best_candidate, best_similarity, verified = find_best_match(
            args.input, candidates, args.threshold
        )

        print()
        print_step("Step 4: Building evidence package...")
        evidence = {
            "person_detected": person,
            "matched_page": best_candidate.get("matched_page", ""),
            "candidate_image": best_candidate.get("candidate_image", ""),
            "candidate_path": best_candidate.get("candidate_path", ""),
            "similarity": best_candidate.get("similarity", best_similarity),
            "verified": verified,
            "threshold": args.threshold,
            "total_candidates_evaluated": len(candidates),
            "best_candidate_index": candidates.index(best_candidate) + 1 if best_candidate in candidates else 0,
            "timestamp": datetime.now().isoformat() + "Z",
            "input_image": args.input
        }

        save_evidence(evidence, evidence_path)

        print()
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*58}{Colors.RESET}")
        print(f"{Colors.BOLD}PIPELINE COMPLETE{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*58}{Colors.RESET}")
        print()
        print(json.dumps(evidence, indent=2))
        print()

        if verified:
            print_success("NEXT STEPS:")
            print("  1. python blockchain/hash_evidence.py")
            print("  2. python blockchain/upload_ipfs.py")
            print("  3. python blockchain/store_evidence.py")
            print("  4. python blockchain/verify_blockchain.py")
            print()
            print_step("Pushing to blockchain automatically...")
            push_to_blockchain(evidence_path)
        else:
            print_warning(
                f"Face not verified (best similarity {best_similarity:.4f} < {args.threshold})."
                f" Try a different input image or lower threshold."
            )

        sys.exit(0 if verified else 2)

    except FileNotFoundError as e:
        print_error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Pipeline failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
