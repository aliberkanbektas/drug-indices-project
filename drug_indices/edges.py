import requests
from rdkit import Chem
from urllib.parse import quote
import json
from typing import List, Optional, Dict, Tuple, Union

def encode_name(name: str) -> str:
    """
    Encode drug name only if it contains spaces.
    Keeps it clean for simple names (like 'afatinib') and encodes when necessary.
    """
    return quote(name) if " " in name else name

def get_edge_list_from_pubchem(drug_name: str, timeout: float = 5.0) -> Optional[List[Tuple[int, int]]]:
    """
    Retrieve the bond-edge list of a molecule from PubChem by entering its name.

    Parameters:
        drug_name (str): The name of the compound to look up on PubChem.
        timeout (float): The number of seconds to wait for an HTTP response before giving up.

    Returns:
        A list of (atom_index1, atom_index2) tuples if successful.
        None on failure (network error, invalid SMILES, etc.).
    """
    url_name = encode_name(drug_name)
    pubchem_url = (f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{url_name}/property/SMILES/TXT")

    try:
        resp = requests.get(pubchem_url, timeout=timeout)
        resp.raise_for_status()
        raw_smiles = resp.text.strip()

    except requests.RequestException as exc:
        print(f"[ERROR] PubChem request failed for '{drug_name}': {exc}")
        return None

    mol = Chem.MolFromSmiles(raw_smiles)
    if mol is None:
        print(f"[ERROR] Invalid SMILES for '{drug_name}': {raw_smiles}")
        return None

    edges: List[Tuple[int, int]] = []
    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()
        edges.append((i, j))

    return edges

def save_edge_relations_to_json(drug_list: List[str], filename: str) -> None:
    """
    Use the PubChem database to query each drug's bond-edge list and save the results to a JSON file.

    Parameters:
        drug_list (List[str]):  a list of compound names.
        filename (str): the path to the output JSON file.
    """
    edge_relations: Dict[str, Union[List[Tuple[int,int]], Dict[str,str]]] = {}
    for name in drug_list:
        result = get_edge_list_from_pubchem(name)
        if result is None:
            edge_relations[name] = {"error": "edge relations not found"}
        else:
            edge_relations[name] = result

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(edge_relations, f)
    print(f"[INFO] Edge relations saved to '{filename}'")


# === Usage ===

if __name__ == "__main__":
    drug_list: List[str] = sorted([
    "afatinib", "alpelisib", "anastrozole", "busulfan", "dasatinib", "daunorubicin",
    "erdafitinib", "melphalan", "mitomycin c", "nilotinib", "olaparib", "orgovyx", "plerixafor",
    "prednisone", "zanubrutinib", "belinostat", "bortezomib", "carmustine", "flutamide",
    "futibatinib", "granisetron", "ibrutinib", "lenalidomide", "lomustine", "midostaurin",
    "olutasidenib", "pomalidomide", "pralatrexate", "repotrectinib", "ribociclib"
    ])
    output_filename: str = "edge_relations.json"
    save_edge_relations_to_json(drug_list, output_filename)
    
