import os
import shutil
from datetime import datetime
from tmtools.io import get_structure, get_residue_data
from tmtools import tm_align
from Bio.PDB import PDBParser, PDBIO, Superimposer
from itertools import combinations
import re

base_dir = input("Drag and drop the folder with pdb files:\n").strip().strip('"')
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_base = f"auto-align-{timestamp}"
os.makedirs(output_base, exist_ok=True)
def extract_prefix(filename):
    match = re.match(r"(e\d+)", os.path.basename(filename))
    return match.group(1) if match else None

for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.isdir(folder_path):
        continue

    grouped_files = {}
    for file in os.listdir(folder_path):
        if file.endswith(".pdb"):
            prefix = extract_prefix(file)
            if prefix:
                full_path = os.path.join(folder_path, file)
                grouped_files.setdefault(prefix, []).append(full_path)

    for prefix, files in grouped_files.items():
        for file1, file2 in combinations(files, 2):
            name1 = os.path.splitext(os.path.basename(file1))[0]
            name2 = os.path.splitext(os.path.basename(file2))[0]

            comparison_subdir = os.path.join(output_base, folder_name, f"{name1}_vs_{name2}")
            os.makedirs(comparison_subdir, exist_ok=True)

            structure1 = get_structure(file1)
            structure2 = get_structure(file2)
            model1 = structure1[0]
            model2 = structure2[0]
            chain1 = next(model1.get_chains())
            chain2 = next(model2.get_chains())

            coords1, seq1 = get_residue_data(chain1)
            coords2, seq2 = get_residue_data(chain2)

            result = tm_align(coords1, coords2, seq1, seq2)

            parser = PDBParser(QUIET=True)
            structure1_bio = parser.get_structure('s1', file1)
            structure2_bio = parser.get_structure('s2', file2)
            model1_bio = structure1_bio[0]
            model2_bio = structure2_bio[0]
            chain1_bio = next(model1_bio.get_chains())
            chain2_bio = next(model2_bio.get_chains())

            residues1 = {r.get_id(): r for r in chain1_bio.get_residues()}
            residues2 = {r.get_id(): r for r in chain2_bio.get_residues()}
            common_res_ids = set(residues1.keys()) & set(residues2.keys())

            atoms1 = []
            atoms2 = []
            for rid in sorted(common_res_ids):
                if 'CA' in residues1[rid] and 'CA' in residues2[rid]:
                    atoms1.append(residues1[rid]['CA'])
                    atoms2.append(residues2[rid]['CA'])

            super_imposer = Superimposer()
            if len(atoms1) == len(atoms2):
                super_imposer.set_atoms(atoms1, atoms2)
                super_imposer.apply(structure2_bio.get_atoms())

                out_pdb = os.path.join(comparison_subdir, "superposed_structure.pdb")
                io = PDBIO()
                io.set_structure(structure2_bio)
                io.save(out_pdb)
            else:
                print(f"⚠️ Skipping {name1} vs {name2}: mismatched CA atoms")
                continue

            txt_path = os.path.join(comparison_subdir, "alignment_results.txt")
            with open(txt_path, 'w') as f:
                f.write(f"TM-score: {result.tm_norm_chain1:.4f}\n")
                f.write(f"RMSD: {result.rmsd:.4f}\n")
                f.write(f"Rotation matrix:\n{result.u}\n")
                f.write(f"Translation vector: {result.t}\n\n")
                f.write("Residue-by-residue comparison:\n")
                for i, (r1, r2) in enumerate(zip(seq1, seq2)):
                    status = "Match" if r1 == r2 else "Mismatch"
                    f.write(f"Residue {i+1}: {r1} vs {r2} - {status}\n")
                f.write("\nSequence 1:\n" + seq1 + "\n")
                f.write("Sequence 2:\n" + seq2 + "\n")

            rasmol_script = f"""
load {os.path.basename(file1)}
load {os.path.basename(file2)}
select all
spacefill
color chain
"""
            with open(os.path.join(comparison_subdir, 'view_superposition.rms'), 'w') as f:
                f.write(rasmol_script)

            shutil.copy(file1, os.path.join(comparison_subdir, os.path.basename(file1)))
            shutil.copy(file2, os.path.join(comparison_subdir, os.path.basename(file2)))

            print(f"✓ Comparing {name1} vs {name2} in {folder_name}/{prefix}/")

print(f"\n✅ Results saved in: {output_base}")
