import json
import networkx as nx
from math import sqrt
import pandas as pd
from typing import Any, Dict, List, Union

def load_edge_relations_from_json(filename: str) -> Dict[str, Union[List[List[int]], Dict[str,str]]]:
    """
    Load the edge relations of multiple drugs from a JSON file.

    Parameters:
        filename (str): The path to the JSON file containing the drug-edge relations.

    Returns:
        Dict[str, Union[List[List[int]], Dict[str, str] A dictionary mapping each drug name
        to either a list of edge pairs or an error dictionary.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_indices(G: nx.Graph) -> Dict[str, float]:
    """
    Compute the following 10 topological indices based on the degree of each pair of connected nodes (edges) in the graph:



        - M1: dx + dy
        - M2: dx * dy
        - mM2: 1/(dx*dy)
        - F: dx^2+dy^2
        - ISI: (dx * dy) / (dx + dy)
        - H: 2 / (dx + dy)
        - SC: sqrt(1 / (dx + dy))
        - HZ: (dx + dy)^2
        - AZ: ((dx * dy) / (dx + dy - 2))^3
        - SDD: dx/dy + dy/dx

    Parameters:
        G (nx.Graph): An undirected graph representing the molecular structure.

    Returns:
        Dict[str, float] A dictionary of computed index names and their values.
    """
    indices = {
        "M1": 0.0, "M2": 0.0, "mM2": 0.0, "FG": 0.0, "ISI": 0.0,
        "H": 0.0, "SC": 0.0, "HM": 0.0, "A": 0.0, "SDD": 0.0
    }

    for x, y in G.edges():
        dx = G.degree[x]
        dy = G.degree[y]
        sum_deg = dx + dy

        indices["M1"]  += sum_deg
        indices["M2"]  += dx * dy
        indices["mM2"] += 1.0 / (dx * dy) if dx*dy != 0 else 0.0
        indices["FG"]   += dx**2 + dy**2
        indices["ISI"] += (dx * dy) / sum_deg if sum_deg != 0 else 0.0
        indices["H"]   += 2.0 / sum_deg if sum_deg != 0 else 0.0
        indices["SC"]  += sqrt(1.0 / sum_deg) if sum_deg != 0 else 0.0
        indices["HM"]  += sum_deg**2
        if sum_deg != 2:
            indices["A"] += ((dx * dy) / (sum_deg - 2))**3
        indices["SDD"] += (dx / dy if dy != 0 else 0.0) + (dy / dx if dx != 0 else 0.0)

    return indices

def calculate_and_return_all_drugs(drug_list: List[str], data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
     For each drug on the list, create a graph for it and calculate its topological indices.

    Parameters:
        drug_list (List[str]): A list of drug names.
        data (Dict[str, Any]): A dictionary containing edge lists or error messages for each drug.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing either calculated indices or error information for each drug.
    """
    results: List[Dict[str, Any]] = []
    for name in sorted(drug_list):
        edges = data.get(name)
        if isinstance(edges, list):
            G = nx.Graph()
            G.add_edges_from(edges)
            raw = calculate_indices(G)
            rounded = {k: round(v, 3) for k, v in raw.items()}
            results.append({"drug": name, "indices": rounded})
        else:
            results.append({"drug": name, "error": edges})
    return results

def save_results_to_dataframe(results: List[Dict[str, Any]], excel_path: str = "drug_indices.xlsx") -> pd.DataFrame:
    """
    Convert the topological index calculation results into a Pandas DataFrame and export them to an Excel file.

    Parameters:
        results (List[Dict[str, Any]]) A list of dictionaries containing drug names and their index values.
        excel_path (str, optional): The file path to save the Excel file. Defaults to 'drug_indices.xlsx'.

    Returns:
        pd.DataFrame: A DataFrame containing drugs as rows and indices as columns.
    """
    valid = [r for r in results if "indices" in r]
    df = pd.DataFrame([r["indices"] for r in valid], index=[r["drug"] for r in valid])
    df.to_excel(excel_path, index=True, engine="openpyxl")
    print(f"[INFO] Drug indices saved to '{excel_path}'")
    return df

# === Usage ===

if __name__ == "__main__":
    drug_list = [
        "afatinib", "alpelisib", "anastrozole", "busulfan", "dasatinib",
        "daunorubicin", "erdafitinib", "melphalan", "mitomycin c",
        "nilotinib", "olaparib", "orgovyx", "plerixafor", "prednisone",
        "zanubrutinib", "belinostat", "bortezomib", "carmustine", "flutamide",
        "futibatinib", "granisetron", "ibrutinib", "lenalidomide",
        "lomustine", "midostaurin", "olutasidenib", "pomalidomide",
        "pralatrexate", "repotrectinib", "ribociclib"
    ]

    data = load_edge_relations_from_json("edge_relations.json")
    results = calculate_and_return_all_drugs(drug_list, data)
    df = save_results_to_dataframe(results, "drug_indices.xlsx")
