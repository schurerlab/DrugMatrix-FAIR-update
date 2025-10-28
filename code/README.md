# Code for DrugMatrix FAIR Update

This directory contains example scripts and small demo data used to illustrate the curation and alignment methods applied in the DrugMatrix FAIR Update project.

---

## ⚙️ Quickstart

```bash
conda env create -f environment.yml
conda activate drugmatrix_fair_demo

python scripts/demo_fuzzy_match.py \
  --file1 demo_data/demo_file1_curated.csv \
  --file2 demo_data/demo_file2_drugmatrix.csv \
  --outprefix demo_data/demo

Outputs:

demo_data/demo_Merged_File1_by_File2_FuzzyMatched.csv

demo_data/demo_Matched_Assay_Scores.csv

---
  
## 📁 Directory Structure

/code
├── environment.yml            # Conda environment for demo
├── scripts/
│   └── demo_fuzzy_match.py    # Fuzzy text-matching demo script
├── demo_data/
│   ├── demo_file1_curated.csv      # Curated table (ChEMBL-style)
│   ├── demo_file2_drugmatrix.csv   # DrugMatrix reference table
│   └── (generated outputs ignored in git)
└── README.md

---
  
## 🧠 Purpose

This code demonstrates how curated ChEMBL-aligned data (File 1) can be mapped to DrugMatrix reference assays (File 2) using text normalization and fuzzy string matching. It represents a simplified version of the alignment workflow used in the FAIR data integration process.

---

## 🔗 Related Repositories

Main Project: DrugMatrix FAIR Update

Data DOI: (to be added once Zenodo release is live)



