# Drug–Target Interaction Dataset Construction

### Replication of *Computational Discovery of Putative Leads for Drug Repositioning through Drug–Target Interaction Prediction* (Coelho et al., 2017)

This repository contains code, and instructions to reproduce the dataset-building methodology described in Coelho et al. (2017), including:

* Extraction of **positive DTI samples** from the Yamanishi dataset
* Construction of **negative DTI samples** from BindingDB and BioLiP
* Integration, filtering, and cleaning of all sources
* Export of final machine-learning-ready datasets

---

## 📁 Repository Structure

```
│
├── notebooks/
│   ├── analyzecsv.ipynb
│   ├── get_negative_dataset.ipynb
│   
│
├── scripts/
│   ├── get_data_scripts.py
│
└── README.md
```

---

## 📘 Overview

This project reproduces the negative and positive drug–target interaction (DTI) datasets used in the Coelho et al. study, following their pipeline as closely as possible.

### **Positive Dataset**

* Collected from the **Yamanishi gold-standard DTI datasets**
* Drug–target pairs with confirmed interaction
* Targets mapped to UniProt identifiers
* Drugs mapped to KEGG/DrugBank IDs

### **Negative Dataset**

The paper defines negative DTIs as **drug–target pairs unlikely to bind**, generated from two sources:

#### 1. **BindingDB (low-affinity interactions)**

* Extract entries with Ki / IC50 / Kd / EC50 **> 10 µM**
* Remove incomplete rows
* Standardize target to UniProt
* Keep minimal schema:

  * `Drug`, `Target`, `Affinity`, `Source`

#### 2. **BioLiP (structural interactions)**

* Parse the raw `.txt` BioLiP file
* Add header
* Extract ligand–protein pairs
* Standardize UniProt IDs
* Same minimal schema as above

#### 3. **Merge & Clean**

* Concatenate BioLiP + BindingDB
* Drop duplicates
* Remove any pair that appears in Yamanishi positives


---

##  Requirements

* Python 3.8+
* pandas
* numpy
* tqdm (optional)
* jupyter / jupyterlab


## Citation

If you use this pipeline, please cite the original paper:

Coelho ED, Arrais JP, Oliveira JL (2017)
*Computational Discovery of Putative Leads for Drug Repositioning through Drug–Target Interaction Prediction.*
**PLOS Computational Biology** 13(10): e1005219.

---

