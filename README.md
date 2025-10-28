# DrugMatrix FAIR Update

This repository hosts the **public landing page and documentation** for the  
**DrugMatrix FAIR-curated in-vitro data release**, prepared for integration with the [ChEMBL database](https://www.ebi.ac.uk/chembl/).

🔗 **Live site:** [https://schurerlab.github.io/DrugMatrix-FAIR-update/](https://schurerlab.github.io/DrugMatrix-FAIR-update/)  
🔗 **GitHub organization:** [Schurer Lab](https://github.com/schurerlab)

---

## 📂 Data Access

- **Small helper files** (≤100 MB) are stored in this repository under [`/data`](./data).  
- **Larger datasets** will be archived in Zenodo with permanent DOIs (links to be added upon release).  
- **Checksums** (SHA-256) for data releases will be provided under [`/checksums`](./checksums).

---

## 🧠 Related Repositories

- **Code repository:** (coming soon) → will contain FAIR curation scripts, schema definitions, and ETL notebooks.  
- **Demo data repository:** (coming soon) → will contain minimal example datasets for public testing and integration demos.

---

## 📖 Citation

- **Dataset:** Cite the Zenodo DOI corresponding to the release.  
- **Software/site:** Cite the repository link above.

---

## ℹ️ About

The **DrugMatrix FAIR Update** project provides curated in-vitro assay data with rich metadata annotations aligned to ontology standards, enabling improved data reuse, integration, and downstream analysis.
# DrugMatrix FAIR Update

The DrugMatrix FAIR Update project provides curated in-vitro assay data with rich metadata annotations aligned to ontology standards, enabling improved data reuse, integration, and downstream analysis.

🔗 **Live site:** [https://schurerlab.github.io/DrugMatrix-FAIR-update/](https://schurerlab.github.io/DrugMatrix-FAIR-update/)

---

## 🧠 Code and Demo Data
The /code directory contains Python scripts, an executable demo, and small example datasets illustrating the curation and alignment workflow used for the DrugMatrix FAIR Update project.
These examples reproduce the text-matching and file-alignment logic applied during data integration between ChEMBL and DrugMatrix.

📁 Explore here: /code

To run the demo locally:

cd code
conda env create -f environment.yml
conda activate drugmatrix_fair_demo
python scripts/demo_fuzzy_match.py \
  --file1 demo_data/demo_file1_curated.csv \
  --file2 demo_data/demo_file2_drugmatrix.csv \
  --outprefix demo_data/demo

Outputs:

demo_data/demo_Merged_File1_by_File2_FuzzyMatched.csv

demo_data/demo_Matched_Assay_Scores.csv
