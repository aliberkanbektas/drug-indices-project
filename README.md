# Drug Topological Indices Calculator

This project retrieves molecular structures of drugs from PubChem and computes a set of graph-based topological indices for each compound. Optionally, users can also visualize the molecular structure as a graph.

## Features

- Retrieves SMILES strings from PubChem  
- Converts SMILES to molecular graphs using RDKit  
- Extracts edge (bond) information from molecules  
- Computes multiple topological indices:
  - M1, M2, mM2, F, ISI, H, SC, HZ, AZ, and SDD  
- Saves results as both JSON (edge data) and Excel (index values)  
- Optional graph visualization using NetworkX and Matplotlib  

## Project Structure

```
drug-indices-project/
├── drug_indices/
│   ├── edges.py          # SMILES retrieval and edge list generation
│   ├── indices.py        # Graph-based topological index calculations
│   └── __init__.py
├── visualization/
│   ├── graph.py          # Optional graph visualization with Matplotlib
│   └── __init__.py
├── main.py               # Script to compute and save all indices
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Ignored files/folders
└── LICENSE               # MIT license
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aliberkanbektas/drug-indices-project_1
   cd drug-indices-project
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

> ⚠️ For full compatibility with RDKit, it's recommended to install it via conda:

```bash
conda install -c conda-forge rdkit
```

## Usage

Run the main pipeline script to compute topological indices for all drugs:

```bash
python main.py
```

This will generate:
- `edge_relations.json` — Atomic connectivity data
- `drug_indices.xlsx`   — Calculated topological indices

## Graph Visualization (Optional)

After running the main script, you can visualize the graph of a single drug:

```bash
python -m visualization.graph
```

Make sure you are in the project root directory before running this command.

## License

This project is licensed under the MIT License.

## Citation

If you use this project, please cite it using the following DOI: 
[![DOI](https://zenodo.org/badge/1024912840.svg)](https://doi.org/10.5281/zenodo.16363897)

