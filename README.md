# 🧬 PDB Batch Structural Aligner
using tmtools

This Python tool allows you to **automatically align and compare multiple PDB structures** within subfolders using **TM-align** and **Bio.PDB**. It performs all-vs-all pairwise superpositions of proteins that share the same prefix (e.g., `e6`, `e7`) within each subfolder and saves the results in a clean, structured format.

---

## 📦 Features

- ✅ Fully automated all-vs-all comparison per subfolder
- 📂 Groups and compares only structures with matching prefixes (e.g., `e6_...`)
- 🧠 Calculates TM-score, RMSD, and per-residue matching
- 🔄 Aligns structures and outputs superposed `.pdb` files
- 📑 Generates text summaries of results
- 📜 Optional RasMol script for visualization
- 🗂️ Organized results per pair in timestamped output folder

---

## 🚀 Usage

1. Clone this repo or copy the script into your project:
   ```bash
   git clone [https://github.com/your-username/pdb-batch-align](https://github.com/flxs007/tmalign-batch-auto).git
   cd pdb-batch-align
   ```
2. Install required dependencies:
   ```bash
   pip install biopython tmtools
   ```
3. Run the script:
   ```bash
   python auto_align.py
   ```
4. When prompted:
   - Drag and drop the base folder containing subfolders of `.pdb` files.
   - Each subfolder should contain `.pdb` files named like `e6_xyz.pdb`, `e7_abc.pdb`, etc.

**Example folder structure:**
```plaintext
input_folder/
├── 58/
│   ├── e6_A.pdb
│   ├── e6_B.pdb
│   ├── e7_X.pdb
│   └── e7_Y.pdb
├── 59/
│   ├── e6_C.pdb
│   └── e6_D.pdb
```

**Output structure:**
```plaintext
auto-align-date/
├── 58/
│   ├── e6_A_vs_e6_B/
│   │   ├── superposed_structure.pdb
│   │   ├── alignment_results.txt
│   │   ├── view_superposition.rms
│   │   ├── e6_A.pdb
│   │   └── e6_B.pdb
│   └── e7_X_vs_e7_Y/
│       └── ...
├── 59/
│   └── e6_C_vs_e6_D/
│       └── ...
```

---

## 📊 Outputs

Each comparison folder contains:
- `superposed_structure.pdb` — The aligned structure
- `alignment_results.txt` — TM-score, RMSD, rotation/translation matrices, and residue comparison
- `view_superposition.rms` — RasMol visualization script
- Original input `.pdb` files

---

## 🧪 Requirements

- [Python 3.7+](https://www.python.org/downloads/release/python-370/)
- [tmtools](https://github.com/jvkersch/tmtools) (for TM-align bindings)
- [biopython](https://biopython.org/) (for structure handling)

---

## ⚠️ Important Notes

- The script compares only chains from the first model and first chain in each structure.
- It automatically skips comparisons where CA atoms do not match between structures.
- Make sure your input `.pdb` files are named consistently with prefixes like `e6`, `e7`, etc., to ensure proper grouping.


**Disclaimer:** This README was generated with the assistance of AI.
