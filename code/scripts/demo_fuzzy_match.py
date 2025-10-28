# scripts/demo_fuzzy_match.py
# Align File 1 (curated) to File 2 (DrugMatrix order) by fuzzy-matching assay-description text.

import argparse
import os
import re
import sys
from typing import Tuple, List, Dict, Any

import pandas as pd
from fuzzywuzzy import process  # optional speedup: pip install python-Levenshtein


# ---------- Helpers ----------

def clean_text(s: Any) -> str:
    """Normalize text for robust matching."""
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s)                # collapse whitespace
    s = s.replace("³H", "3H")                 # normalize ³H → 3H
    s = s.replace("–", "-").replace("−", "-") # en dash/minus → hyphen
    return s


def load_any(path: str) -> pd.DataFrame:
    """Load CSV or Excel by extension."""
    ext = os.path.splitext(path.lower())[1]
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    return pd.read_csv(path)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim and remove invisible chars in headers."""
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\u00A0", " ", regex=False)  # non-breaking space
        .str.replace("\r", "", regex=False)
        .str.replace("\n", "", regex=False)
    )
    return df


# ---------- Core ----------

def fuzzy_align(
    file1: pd.DataFrame,
    file2: pd.DataFrame,
    file1_key: str,
    file2_key: str,
    threshold: int = 81
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Return (merged_rows, audit_log).
    merged_rows = File1 rows reordered to follow File2 via fuzzy matches on cleaned text.
    audit_log  = per-row scores and matches (including no-match cases).
    """
    # Build clean keys
    f1 = file1.copy()
    f2 = file2.copy()
    f1["clean_key"] = f1[file1_key].apply(clean_text)
    f2["clean_key"] = f2[file2_key].apply(clean_text)

    # Index map for quick row retrieval
    f1_map = f1.set_index("clean_key")
    f1_keys: List[str] = list(f1_map.index)
    f1_cols = [c for c in f1.columns if c != "clean_key"]

    rebuilt_rows = []
    audit: List[Dict[str, Any]] = []

    print(f"[INFO] Matching with threshold ≥ {threshold} …")
    for target in f2["clean_key"]:
        if not f1_keys:
            match, score = ("", 0)
        else:
            match, score = process.extractOne(target, f1_keys)

        if score >= threshold:
            print(f"[MATCH] {target!r} → {match!r} (score: {score})")
            rebuilt_rows.append(f1_map.loc[[match]][f1_cols])
            audit.append(
                {
                    "File2 Assay Description (clean)": target,
                    "Matched File1 Assay (clean)": match,
                    "Match Score": score,
                }
            )
        else:
            print(f"[NO-MATCH] {target!r} (best score: {score})")
            audit.append(
                {
                    "File2 Assay Description (clean)": target,
                    "Matched File1 Assay (clean)": None,
                    "Match Score": score,
                }
            )

    merged = pd.concat(rebuilt_rows, ignore_index=True) if rebuilt_rows else pd.DataFrame()
    audit_df = pd.DataFrame(audit)
    return merged, audit_df


# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Reorder File 1 rows to follow File 2 assay order using fuzzy match on cleaned text."
    )
    ap.add_argument("--file1", required=True, help="Path to File 1 (curated; CSV or Excel)")
    ap.add_argument("--file2", required=True, help="Path to File 2 (DrugMatrix reference; CSV or Excel)")
    ap.add_argument(
        "--file1_key",
        default="chembl_assay_description",
        help="Column in File 1 containing assay description (default: chembl_assay_description)",
    )
    ap.add_argument(
        "--file2_key",
        default="Assay Description",
        help="Column in File 2 containing assay description (default: 'Assay Description')",
    )
    ap.add_argument(
        "--threshold",
        type=int,
        default=81,
        help="Fuzzy match acceptance threshold (0–100). Default 81.",
    )
    ap.add_argument(
        "--outprefix",
        default="demo_output",
        help="Prefix for output files (default: demo_output)",
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    # Load
    print(f"[INFO] Loading File 1: {args.file1}")
    f1 = load_any(args.file1)
    print(f"[INFO] Loading File 2: {args.file2}")
    f2 = load_any(args.file2)

    # Normalize columns
    f1 = normalize_columns(f1)
    f2 = normalize_columns(f2)

    # Validate key columns
    if args.file1_key not in f1.columns:
        raise KeyError(
            f"File 1 key column '{args.file1_key}' not found. Columns: {f1.columns.tolist()}"
        )
    if args.file2_key not in f2.columns:
        raise KeyError(
            f"File 2 key column '{args.file2_key}' not found. Columns: {f2.columns.tolist()}"
        )

    # Align
    merged, audit = fuzzy_align(
        file1=f1, file2=f2, file1_key=args.file1_key, file2_key=args.file2_key, threshold=args.threshold
    )

    # Output paths
    outdir = os.path.dirname(args.outprefix) or "."
    os.makedirs(outdir, exist_ok=True)
    audit_path = f"{args.outprefix}_Matched_Assay_Scores.csv"

    # Save audit first (always useful)
    audit.to_csv(audit_path, index=False)
    print(f"[SAVE] {audit_path}")

    # Save merged table if we have matches
    if not merged.empty:
        merged_path = f"{args.outprefix}_Merged_File1_by_File2_FuzzyMatched.csv"
        merged.to_csv(merged_path, index=False)
        print(f"[SAVE] {merged_path}")
    else:
        print("[WARN] No matches ≥ threshold — merged file not written.")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # Safe exit if piping output
        try:
            sys.stdout.close()
        except Exception:
            pass
        try:
            sys.stderr.close()
        except Exception:
            pass

