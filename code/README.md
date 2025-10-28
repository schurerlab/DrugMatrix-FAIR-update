# Code for DrugMatrix FAIR Update

## Quickstart
```bash
conda env create -f environment.yml
conda activate drugmatrix_fair_demo

python scripts/demo_fuzzy_match.py \
  --file1 demo_data/demo_file1_curated.csv \
  --file2 demo_data/demo_file2_drugmatrix.csv \
  --outprefix demo_data/demo

